# Patching And Dependency Tooling

Index: composer-patches, PHPStan/PHPCS pinning, ecs-fix, shopware-rector, Frosh Tools, mysqldump canonical form, security auditing.

## `cweagans/composer-patches` For Vendor Patches

Never edit `vendor/` directly. Changes disappear on `composer update` and are absent from CI.

Setup:

```bash
composer require cweagans/composer-patches:^1.7
```

Create the patch:

```bash
git diff path/to/vendor/file.php > custom/patches/short-descriptive-name.patch
```

Declare in root `composer.json`:

```json
{
  "extra": {
    "patches": {
      "shopware/core": {
        "Descriptive name of the fix": "custom/patches/short-descriptive-name.patch"
      }
    }
  }
}
```

Patches apply automatically on `composer install` / `composer update`. Commit the patch file. When Shopware ships the fix upstream, remove the patch entry.

## Backport Policy

Some Shopware fixes ship only in 6.7 (or a specific 6.7.x) and are not backported to 6.6. Example: `shopware/shopware` PR #18205 (language active-filter fix) is only in 6.7.13.0+.

- Check the PR's target branches on GitHub before assuming a 6.6 backport exists.
- If a fix you need is 6.7-only and the project runs 6.6, use `composer-patches` to backport locally.
- Document each patch with the upstream URL and the version where it can be removed.

## PHPStan And PHP-CS-Fixer Pinning

Pin analysis tools to the versions Shopware core is tested against. Mismatched versions produce false positives on core-installed extensions.

Current recommendation (verify against Shopware's own `composer.json` for the target 6.7.x):

```json
{
  "require-dev": {
    "phpstan/phpstan": "1.12.5",
    "phpstan/phpstan-symfony": "1.4.10",
    "friendsofphp/php-cs-fixer": "3.64.0"
  }
}
```

Run PHPStan with a raised memory limit and scoped paths (never analyze `vendor/`):

```bash
vendor/bin/phpstan analyse --memory-limit=2G custom/plugins/YourPlugin/src
```

Answer "yes" to Composer's PHPStan extension-installer trust prompt or extensions (like `phpstan-symfony`) won't register.

Wire php-cs-fixer through an `ecs-fix` composer script:

```json
{
  "scripts": {
    "ecs-fix": "vendor/bin/php-cs-fixer fix custom/plugins/YourPlugin/src",
    "phpstan": "vendor/bin/phpstan analyse --memory-limit=2G custom/plugins/YourPlugin/src"
  }
}
```

Remediate per-plugin / per-folder, not project-wide. Project-wide initial baselines produce merge conflicts on every branch.

## `FriendsOfShopware/shopware-rector`

Rector rule sets for Shopware upgrades. Run on every major-version upgrade.

Install:

```bash
composer require --dev friendsofshopware/shopware-rector
```

Config:

```php
// rector.php
use Rector\Config\RectorConfig;
use FriendsOfShopware\ShopwareRector\Set\ShopwareSetList;

return static function (RectorConfig $rectorConfig): void {
    $rectorConfig->paths([__DIR__ . '/custom/plugins/YourPlugin/src']);
    $rectorConfig->sets([ShopwareSetList::SHOPWARE_6_7_0]);
};
```

Run: `vendor/bin/rector process`.

Relevant `SHOPWARE_6_7_0` rules include:

- `InterfaceReplacedWithAbstractClassRector` — migrates deprecated interfaces (like `AsyncPaymentHandlerInterface`) to `AbstractPaymentHandler`.
- `AddArgumentToClassWithoutDefaultRector` — adds new required constructor args (e.g., `LoggerInterface` on `ScheduledTaskHandler`).
- `MakeClassConstructorArgumentRequiredRector` — flags previously-optional args now required.
- `ThumbnailGenerateSingleToMultiGenerateRector` — thumbnail API migration.

For 6.5 legacy work still in flight: `MigrateCaptchaAnnotationToRouteRector`, `MigrateLoginRequiredAnnotationToRouteRector`, `MigrateRouteScopeToRouteDefaults`, `ContextMetadataExtensionToStateRector`, `FakerPropertyToMethodCallRector`.

## `FriendsOfShopware/FroshTools`

Install on every non-trivial 6.x project for in-admin observability:

- cache pool status
- Messenger transport queues (Doctrine, Redis, AMQP) with counts
- scheduled task list, last run, and next run
- `var/log/` recent errors
- Elasticsearch indices, aliases, and mapping snapshots
- feature-flag list with current state
- registered webhooks
- state machine dumps
- Fastly integration status

Install: `composer require frosh/tools`. Enable in admin.

Queue-count endpoint (Admin API): `GET /api/_action/frosh-tools/queue/list`.

Known caveat: in 6.6 the per-message-type counters can be wrong. Only the `messenger.transport.{xyz}` counters are reliable in 6.6. In 6.7 both are reliable.

## MySQL Dump Canonical Form

For consistent, portable Shopware DB dumps:

```bash
mysqldump \
  --compress \
  --routines \
  --hex-blob \
  --single-transaction \
  --no-tablespaces \
  <database> \
  | sed -e 's/DEFINER[ ]*=[ ]*[^*]*\*/\*/' \
  > dump.sql
```

Every flag matters:

- `--compress` reduces wire load on remote dumps.
- `--routines` includes stored procedures/functions plugin migrations may install.
- `--hex-blob` writes binary columns safely.
- `--single-transaction` produces a consistent snapshot on a live DB.
- `--no-tablespaces` avoids `PROCESS` privilege errors on managed DBs.
- The `sed` pipeline strips `DEFINER=` clauses. Without stripping, dumps embed the source DB user and imports fail on target DBs.

## Security Audit

Run before every release:

```bash
composer audit
composer show --outdated --direct
```

Address deprecated dependencies. Most audit findings are resolved by updating to the latest Shopware patch on the current minor.

## What Not To Do

- Do not commit `auth.json` with production Shopware Store keys. Prefer env-var injection at build time. (Shopware Store composer keys grant read-only access to plugin source and are not high-value secrets, so keep out of repo when possible but do not treat presence as a P0 leak.)
- Do not disable PHPStan extension installer prompts globally. Trust per-project.
- Do not run Rector against `vendor/`. Scope to `custom/plugins/*/src`.

## Sources

- Rune Laenen laenen.me blog posts on PHPStan setup, composer-patches, and mysqldump.
- FriendsOfShopware GitHub org.
- Shopware `composer.json` for tested tool versions.
