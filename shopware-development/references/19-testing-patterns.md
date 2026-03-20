# Testing Patterns

## Test Scope

Pick the narrowest test that still proves the behavior:

- unit tests for pure services, mappers, validators, and retry logic
- integration tests for DAL definitions, decorators, migrations, and service wiring
- Store API or HTTP-level tests for customer-facing routes and checkout behavior
- command tests for Symfony console entry points

## Core Shopware Test Traits

- Use `IntegrationTestBehaviour` when the code needs the kernel, container, and DB transaction isolation.
- Use `SalesChannelApiTestBehaviour` when the behavior is best proven through Store API routes.
- Use `KernelTestBehaviour` for service or command tests that do not need database-heavy setup.
- Keep test bootstrap behavior aligned with Shopware's plugin test bootstrap patterns instead of ad hoc kernel boot code.

Example patterns:

```php
// Bad: plain PHPUnit test with manual container boot and persistent shared fixtures
final class ProductServiceTest extends TestCase
{
    protected function setUp(): void
    {
        $this->kernel = new Kernel('test', true);
        $this->kernel->boot();
    }
}
```

```php
// Preferred: Shopware integration trait with test-local fixture setup
final class ProductServiceTest extends TestCase
{
    use IntegrationTestBehaviour;

    public function testCreatesProduct(): void
    {
        $repository = $this->getContainer()->get('product.repository');
        $context = Context::createDefaultContext();

        $repository->create([['id' => Uuid::randomHex(), 'productNumber' => 'P-' . Uuid::randomHex()]], $context);

        static::assertTrue(true);
    }
}
```

## Fixtures and Builders

- Build only the data the test needs.
- Keep reusable product, customer, and order builders small and explicit.
- Avoid global shared fixtures that make tests order-dependent or hard to reason about.
- Use transaction rollback from the Shopware test traits instead of hand-written cleanup where possible.

## Repository Mocks

- Prefer `StaticEntityRepository` or equivalent Shopware-friendly patterns for unit tests that need repository-like behavior without full DAL integration.
- Do not mock DAL internals so deeply that the test only proves the mock arrangement.

```php
// Preferred: static repository in a unit test boundary
$repository = new StaticEntityRepository([
    ['id' => $customerId, 'email' => 'test@example.com'],
]);
```

## Store API and Checkout Tests

- Use `SalesChannelApiTestBehaviour` or request-level tests for custom Store API routes, cart mutations, and checkout behavior.
- For cart or checkout changes, verify both success and rejection paths.
- If pricing, tax, shipping, or payment method selection changes, prove the behavior through a sales-channel-aware test instead of only testing one service in isolation.

## Migration and Wiring Tests

- Integration-test destructive schema assumptions, backfill orchestration, and new indexes when the migration risk is real.
- After adding decorators, handlers, or scheduled tasks, run at least one boot-path or container-compilation check.
- If a migration changes entity structure, add one integration test that proves the repository shape still works after boot.

## Admin and Frontend Notes

- Keep admin E2E coverage targeted. Use it when build/runtime behavior matters more than isolated service logic.
- For storefront-heavy work, use smoke checks and targeted browser verification where performance or accessibility risk is real, but keep the primary ownership of browser-accessibility rules in `17-accessibility-and-template-best-practices.md`.
