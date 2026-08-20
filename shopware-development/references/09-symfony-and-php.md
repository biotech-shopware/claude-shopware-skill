# Symfony and PHP

## Symfony Rules That Matter in Shopware

- Prefer constructor injection and explicit service dependencies.
- Keep services private unless they are meant to be fetched as public entry points.
- Organize business logic into small services with clear boundaries.
- Use service decoration or composition instead of patching third-party code.
- Wrap external HTTP access with Symfony HttpClient-based services that define timeouts and, where appropriate, retry policy.
- Use Messenger for asynchronous work instead of inventing custom background loops.
- Use Monolog channels and structured context without leaking secrets.

Example patterns:

```php
// Bad: runtime service lookup and hidden coupling
final class SyncController
{
    public function __invoke(ContainerInterface $container): Response
    {
        $client = $container->get(MyPspClient::class);
        $client->sync();

        return new Response();
    }
}
```

```php
// Preferred: explicit dependency graph and thin entry point
final class SyncController
{
    public function __construct(private readonly SyncService $syncService)
    {
    }

    public function __invoke(): Response
    {
        $this->syncService->sync();

        return new Response();
    }
}
```

```php
// Preferred: timeout-bounded HttpClient wrapper
final class ProviderClient
{
    public function __construct(private readonly HttpClientInterface $httpClient)
    {
    }

    public function fetchStatus(string $reference): array
    {
        return $this->httpClient->request('GET', '/status/' . $reference, [
            'timeout' => 5,
        ])->toArray();
    }
}
```

## PHP Baseline

Apply these rules unless the project has a stricter local standard:

- declare strict types in PHP files
- prefer DRY and KISS over defensive ceremony
- use typed parameters, properties, and return types
- model structured domain data explicitly when arrays become ambiguous
- keep public APIs clear about nullability and failure modes
- use exceptions for exceptional flows, not normal branching
- prefer immutable or append-only patterns for state that is replayed or retried
- use parameterized SQL when DAL is not suitable
- avoid hidden global state and runtime service lookups
- avoid redundant normalization, casting, or fallback branches when the contract already guarantees the value

Example patterns:

```php
// Bad: defensive wrappers after the contract already guarantees a non-null string
$code = trim((string) $requestDto->getWebhookCode());
```

```php
// Preferred: use the typed contract directly
$code = $requestDto->getWebhookCode();
```

## Shopware-Specific Translation of These Rules

- Symfony service discipline maps directly to Shopware plugin service design.
- HttpClient and Messenger guidance matter most for external APIs, webhooks, imports, and payment providers.
- Logging rules matter most for admin operations, background workers, and payment flows where PII and secrets are easy to leak.
- PHP typing and explicit domain models matter most around DAL payloads, provider adapters, and custom entity state.
- Keep framework examples aligned with Shopware extension points. If a Symfony pattern fights Shopware's route scopes, DAL, or state handlers, choose the Shopware-compatible variant.
- If a safeguard is needed, tie it to a concrete failure mode in the actual Shopware code path instead of adding hypothetical protection everywhere.

## 6.7 Runtime And Framework Notes

### Symfony And PHP Versions

- Symfony 7.3 baseline from Shopware 6.7.2.
- Symfony 7.4 from 6.7.7.
- PHP 8.2 minimum, 8.4 default recommended, 8.5 supported from 6.7.6+.
- Recent patches drop 8.3 from the tested matrix. Avoid 8.3-only syntax.
- `php-redis` extension v6.1+ required from 6.7.7.

Source: release notes 6.7.2, 6.7.6, 6.7.7.

### Constraints Use Named Arguments

Symfony validator constraint constructors take named arguments instead of options arrays.

```php
// Bad
$constraint = new CustomerEmailUnique(['salesChannelContext' => $context]);

// Preferred
$constraint = new CustomerEmailUnique(salesChannelContext: $context);
```

Source: UPGRADE-6.7.md §6.7.3.0.

### `ResetInterface` For Long-Running Runtimes

FrankenPHP and RoadRunner keep worker processes alive across requests. Services holding request-scoped state must implement `Symfony\Contracts\Service\ResetInterface::reset()` to clear it.

```php
final class RequestContextCache implements ResetInterface
{
    private array $cache = [];

    public function reset(): void
    {
        $this->cache = [];
    }
}
```

Applies to per-request caches, current-context wrappers, per-request idempotency guards, and anything else that must not leak across requests.

Source: release notes 6.7.2.
