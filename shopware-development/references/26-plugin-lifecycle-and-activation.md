# Plugin Lifecycle and Activation

Index: why this class of defect is invisible, lifecycle methods, the version chain, what needs a bump, migrations, `updateDestructive()`, fresh-install vs update, deployment ordering, review prompts.

## Why This Class Of Defect Is Invisible

A change that only executes from a plugin lifecycle hook can merge, deploy, and never run — and fail **only on already-installed systems**. A fresh install runs `install()`, so the code works in every local setup, every CI run, and every new environment. The defect appears only on the shops that already had the plugin.

Nothing in a normal test suite catches this. Treat "does this need a version bump to take effect?" as a required review question, not a deployment detail.

## Lifecycle Methods

`Plugin.php` defines exactly seven overridable methods:

`install` · `postInstall` · `update` · `postUpdate` · `activate` · `deactivate` · `uninstall`

- **There is no `postActivate()` method.** `PluginPostActivateEvent` exists as an event, but there is nothing to override.
- `activate()` and `deactivate()` run *before* the state change.
- Fresh install runs `install()` → `postInstall()`. Update runs `update()` → `postUpdate()`. `update()` never runs on a fresh install.
- Inside `PluginLifecycleService::installPlugin()` the exact order is `install()` → plugin migrations → custom-field XML sync → `postInstall()`. Tables a migration creates **do not exist yet in `install()`**. Seed data that needs them (mail templates, flows, default records) in the migration itself or in `postInstall()`. A migration that inserts mail templates therefore also runs on a fresh install.

### What Does Not Run On Activate

- **Migrations do not run.** `activatePlugin()` sets `setAutoMigrate(false)` before calling `activate()`, so `runMigrations()` returns at its guard. Same on deactivate and uninstall.
- **Custom-field XML sync does not run.** It happens only on install and update.

Do not rely on activation to apply schema or field changes.

## The Version Chain

```
composer.json version bump
  → bin/console plugin:refresh        writes upgrade_version when filesystem version > DB version
  → upgrade_version > version         plugin is now considered updatable
  → bin/console plugin:update <Name>  runs update() + migrations + custom-field sync
  → version = upgrade_version, upgrade_version = null, upgraded_at = now()
```

Two details that change how you debug this:

**`PluginLifecycleService::updatePlugin()` has no version guard.** It computes the target as `getUpgradeVersion() ?? getVersion()` and runs everything regardless. The gate is in the callers, and they disagree:

| Caller | Version-gated? |
| --- | --- |
| `plugin:update:all` | Yes — skips when `upgradeVersion === null`, **and skips inactive plugins** |
| Deployment Helper | Yes |
| `bin/console plugin:update <Name>` | **No** — runs on any installed plugin |

So a targeted `plugin:update <Name>` will run `update()` without a bump, while the automated paths will not. Use that to force a sync when debugging; do not rely on it in deployment.

**For Composer-managed plugins in `vendor/`, editing `composer.json` is not enough.** The version comes from the resolved package in `composer.lock` — run `composer update` for the new version to be visible at all.

The same applies to the plugin's **name and description** (`extra.label`, `extra.description`). `PluginFinder` takes Composer-managed plugins from Composer's installed-package data. A local copy in `custom/plugins/` wins, but `custom/static-plugins/` path packages are not local copies. After renaming a static plugin, run `composer update <package>` and then `plugin:refresh` before the admin shows the new label.

## What Needs A Version Bump To Reach Production

Anything invoked from `update()` or `postUpdate()`:

- custom-field installers (both the declarative XML and hand-written installer services)
- entity/config installers and default-config seeding
- data backfills and repair routines
- new migrations, in practice — see below

## Migrations

Migration *identity* is the timestamp: `getCreationTimestamp()` keys the run-once record, not the plugin version. But migration *execution* on a deployed system happens through the plugin update flow. Without a bump, the automated paths skip the plugin and new migrations do not run either.

Manual escape hatch:

```bash
bin/console database:migrate <BundleName> --all
```

## `updateDestructive()` Never Runs For Plugins

Put every change the plugin needs into `update()`.

`PluginLifecycleService::runMigrations()` calls `migrateInPlace()`, which reaches `MigrationRuntime::migrate()` — and that calls `update()` only. `updateDestructive()` is reachable solely from `migrateDestructiveInPlace()`, called only by `bin/console database:migrate-destructive`, which merchants and platforms effectively never run for plugins.

It exists for core's deferred-destruction model: `getExecutableDestructiveMigrations()` selects rows `WHERE update IS NOT NULL AND update_destructive IS NULL`, so destructive work runs in a later pass gated on Shopware *major* versions. There is no plugin analogue.

Handle removal in `uninstall()` instead.

Related trap: `MigrationStep::isInstallation()` reads the `SHOPWARE_INSTALL` env var — the **core** install flag, not "my plugin is installing". Do not branch plugin migration behavior on it.

## Fresh Install vs Update — Behavioral Differences

- `install()` syncs custom fields with `deleteMissingXml: false`; `update()` syncs with `deleteMissingXml: true`. The update path **deletes** field sets and fields the plugin previously declared and has since dropped from the XML.
- A re-install does not run `update()`. `installPlugin()` promotes a pending `upgradeVersion` into `version` first, then runs `install()`.
- Declarative `custom-fields.xml` at `Resources/config/custom-fields.xml` is available from **6.7.13.0**. Before that, use an installer service called from the lifecycle hooks.

## Deployment Ordering

`plugin:refresh` must come before any plugin lifecycle command:

```
plugin:refresh
plugin:install → plugin:update → plugin:deactivate → plugin:remove
theme:compile
cache clear
```

Two gotchas:

- **`plugin:install --activate --refresh` silently skips activation** — it prints "Can not refresh and activate in same request." Run `plugin:refresh` as its own command first.
- **Cache is not cleared automatically.** Without `-c`, lifecycle commands only print a reminder.

## Review Prompts

- Does this change run from a lifecycle hook? If so, is there a version bump in the same diff?
- Is the plugin in `vendor/`? Then is there a `composer.lock` change too, not just `composer.json`?
- Was this tested on an already-installed system, or only on a fresh install?
- Does any required work sit in `updateDestructive()`?
- Does the diff drop a field from `custom-fields.xml` that the update path will now delete from existing shops?
- Does the deployment run `plugin:refresh` before `plugin:update`?
