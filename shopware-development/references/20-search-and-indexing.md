# Search and Indexing

Index: search rules, mapping/fetch symmetry, indexer lifecycle, workers, query builders, operations, review prompts.

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
- Implement the complete `EntityIndexer` contract for 6.6 and 6.7: `getName()`, `iterate()`, `update()`, `handle()`, `getTotal()`, and `getDecorated()`.
- If an indexer write would re-trigger indexing, use direct DBAL writes inside `handle()` or add the `EntityIndexerRegistry::DISABLE_INDEXING` state deliberately before writing through DAL.
- If an indexer change implies a full rebuild, name that in rollout guidance and QA notes.

Example patterns:

```php
final class ExampleIndexer extends EntityIndexer
{
    public function __construct(
        private readonly IteratorFactory $iteratorFactory,
        private readonly EntityRepository $repository,
        private readonly ExampleIndexUpdater $updater
    ) {
    }

    public function getName(): string
    {
        return 'my_plugin.example.indexer';
    }

    public function iterate(?array $offset): ?EntityIndexingMessage
    {
        $iterator = $this->iteratorFactory->createIterator($this->repository->getDefinition(), $offset);
        $ids = $iterator->fetch();

        if ($ids === []) {
            return null;
        }

        return new EntityIndexingMessage(array_values($ids), $iterator->getOffset());
    }

    public function update(EntityWrittenContainerEvent $event): ?EntityIndexingMessage
    {
        $ids = $event->getPrimaryKeys(CustomerDefinition::ENTITY_NAME);
        if ($ids === []) {
            return null;
        }

        return new EntityIndexingMessage(array_values($ids), null, $event->getContext());
    }

    public function handle(EntityIndexingMessage $message): void
    {
        $ids = $message->getData();
        if (!\is_array($ids)) {
            return;
        }

        $ids = array_values(array_unique(array_filter($ids)));
        if ($ids === []) {
            return;
        }

        $this->updater->update($ids, $message->getContext());
    }

    public function getTotal(): int
    {
        return $this->iteratorFactory->createIterator($this->repository->getDefinition())->fetchCount();
    }

    public function getDecorated(): EntityIndexer
    {
        throw new DecorationPatternException(static::class);
    }
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

## Reindexing Endpoint With `only` Parameter

Undocumented but works reliably: `POST /api/_action/indexing` with a JSON body targeting specific indexers.

```bash
curl -X POST https://shop.example.com/api/_action/indexing \
    -H "Authorization: Bearer <admin-token>" \
    -H "Content-Type: application/json" \
    -d '{"only": ["category.indexer"]}'
```

- Returns `204 No Content`.
- The `only` parameter schedules the indexing on the queue rather than running inline. Requires workers to be consuming.
- Use for targeted rebuilds — e.g., a plugin migration that only affects category cache, without triggering a full `dal:refresh:index`.

Source: real-world Slack thread, `#altus-nova_shopware`, August 2026.

## Elasticsearch Env Vars

Production settings for 6.7:

- `SHOPWARE_ES_THROW_EXCEPTION=1` — fail loudly on ES outage instead of silently falling back to MySQL and melting the primary.
- `SHOPWARE_ES_USE_LANGUAGE_ANALYZER=1` (6.7.11+) — enable language-specific analyzers.
- `SHOPWARE_ADMIN_ES_ENABLED=1` and `ENABLE_OPENSEARCH_FOR_ADMIN_API=1` — enable admin ES. Then run `bin/console es:admin:index`.

Source: release notes 6.7.5, 6.7.11; developer.shopware.com performance tweaks.

## Queue Statistics With Frosh Tools

Queue counts for indexing progress:

- `GET /api/_action/frosh-tools/queue/list` (via `FriendsOfShopware/FroshTools`).
- 6.6 caveat: per-message-type counters can be wrong. Only the `messenger.transport.{xyz}` counters are reliable in 6.6. In 6.7 both are reliable.

Full observability tooling in `25-patching-and-dependency-tooling.md`.
