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
- use typed parameters, properties, and return types
- model structured domain data explicitly when arrays become ambiguous
- keep public APIs clear about nullability and failure modes
- use exceptions for exceptional flows, not normal branching
- prefer immutable or append-only patterns for state that is replayed or retried
- use parameterized SQL when DAL is not suitable
- avoid hidden global state and runtime service lookups

## Shopware-Specific Translation of These Rules

- Symfony service discipline maps directly to Shopware plugin service design.
- HttpClient and Messenger guidance matter most for external APIs, webhooks, imports, and payment providers.
- Logging rules matter most for admin operations, background workers, and payment flows where PII and secrets are easy to leak.
- PHP typing and explicit domain models matter most around DAL payloads, provider adapters, and custom entity state.
- Keep framework examples aligned with Shopware extension points. If a Symfony pattern fights Shopware's route scopes, DAL, or state handlers, choose the Shopware-compatible variant.
