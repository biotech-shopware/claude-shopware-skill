# Search and Indexing

## Search Rules

- Prefer Shopware's search and listing routes when the task is storefront search or filtering behavior.
- Use DAL reads for bounded backoffice or support tasks, not as a substitute for storefront search architecture.
- Treat Elasticsearch or OpenSearch extension points as mapping plus fetch plus query responsibilities together. Do not modify only one side.
- For existing entities, prefer subscribing to existing write events when that solves the requirement. Add a custom indexer only when the data really needs indexed batch rebuild behavior.

Example patterns:

```php
// Bad: raw DAL search used as a storefront search system
$criteria = new Criteria();
$criteria->addFilter(new ContainsFilter('name', $term));

return $this->productRepository->search($criteria, $context);
```

```php
// Preferred: use Shopware search or listing routes so the configured search backend stays authoritative
return $this->productSearchRoute->load(
    new Request(['search' => $term]),
    $salesChannelContext,
    (new Criteria())->setLimit(24)
)->getListingResult();
```

## Mapping and Fetch Symmetry

- If you extend indexed fields, update mapping and fetch behavior together.
- Keep mapped fields bounded and purpose-driven. Do not stuff large blobs or low-value debug data into the index.
- Preserve language, sales-channel, and visibility semantics when extending indexed data.
- When decorating existing indexers or Elasticsearch definitions, keep the change additive and compatible with the decorated service.

```php
// Preferred: extend mapping and fetch together through decoration
public function mapping(array $mapping): array
{
    $mapping = $this->inner->mapping($mapping);
    $mapping['properties']['myField'] = AbstractElasticsearchDefinition::KEYWORD_FIELD;

    return $mapping;
}
```

## Entity Indexer Lifecycle

- Register custom indexers with the `shopware.entity_indexer` tag.
- `iterate()` owns full rebuild chunking. Keep it bounded with `IteratorFactory` so `bin/console dal:refresh:index` can process large data sets safely.
- `update()` should emit `EntityIndexingMessage` only for the changed IDs that actually need recomputation.
- `handle()` runs on the worker path. Re-read current state there instead of trusting stale serialized entities.
- If an indexer write would re-trigger indexing, use direct DBAL writes inside `handle()` or add the `EntityIndexerRegistry::DISABLE_INDEXING` state deliberately before writing through DAL.
- If an indexer change implies a full rebuild, name that in rollout guidance and QA notes.

Example patterns:

```php
final class ExampleIndexer extends EntityIndexer
{
    public function __construct(
        private readonly IteratorFactory $iteratorFactory,
        private readonly EntityRepository $repository
    ) {
    }

    public function getName(): string
    {
        return 'my_plugin.example.indexer';
    }

    public function iterate($offset): ?EntityIndexingMessage
    {
        $iterator = $this->iteratorFactory->createIterator($this->repository->getDefinition(), $offset);
        $ids = $iterator->fetch();

        if ($ids === []) {
            return null;
        }

        return new EntityIndexingMessage(array_values($ids), $iterator->getOffset());
    }
}
```

```php
public function update(EntityWrittenContainerEvent $event): ?EntityIndexingMessage
{
    $ids = $event->getPrimaryKeys(CustomerDefinition::ENTITY_NAME);
    if ($ids === []) {
        return null;
    }

    return new EntityIndexingMessage(array_values($ids), null);
}
```

```php
// services.php
$services->set(ExampleIndexer::class)->tag('shopware.entity_indexer');
```

## Reindexing and Worker Discipline

- `bin/console dal:refresh:index` is the full-rebuild path. Treat it as an operational event, not a casual side effect of deployment.
- Keep indexer messages small. Store IDs and minimal context only.
- If indexing work can pile up behind checkout-sensitive messages, split transports or worker consumption accordingly.
- Document fallback behavior when Elasticsearch or OpenSearch is stale, disabled, or rebuilding.

## Query Builder Customization

- Extend product search query builders or search decorators instead of bypassing the configured search backend with raw SQL.
- Keep custom scoring, term expansion, and boosted fields explicit and measurable.
- If the project must support fallback to MySQL, make the degraded behavior explicit and observable.

## Reindexing and Operations

- Mapping changes require a reindex strategy. Do not ship mapping changes without naming the reindex implication.
- Keep index updates and batch jobs bounded.
- If the project uses admin OpenSearch or search-specific flags, document the opt-in or fallback behavior in release notes and QA guidance.
- When search behavior changes, verify both correctness and operational blast radius: index size, rebuild time, and fallback behavior.
- When a plugin writes data that a custom indexer depends on, verify the write event, message emission, worker consumption, and search result all line up end to end.

## Review Prompts

- Is storefront search using the correct route or backend abstraction?
- If a field is added to the index, is fetch logic updated to populate it?
- Does the custom search logic preserve language, visibility, and sales-channel scope?
- What happens when Elasticsearch or OpenSearch is disabled or stale?
- Is any search change going to force reindexing, and is that captured in rollout guidance?
