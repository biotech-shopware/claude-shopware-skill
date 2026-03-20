# CLI and Dev Tooling

## Console Commands

- Build commands with Symfony console conventions: clear name, description, arguments, options, and help text.
- Keep commands orchestration-only; business logic belongs in services.
- Support `--dry-run`, bounded execution, and confirmation prompts for expensive operations.
- Use `SymfonyStyle` and progress output for long-running work.
- Chunk large operations instead of loading everything into memory.
- Do not spawn internal sync or maintenance work via `Symfony Process` from controllers or services just to run your own commands. Use Messenger, scheduled tasks, or invoke the service directly.

Example:
- a sync command
  Accept IDs optionally, add `--limit` and `--since`, confirm large runs, and report a compact success/failure summary.

```php
// Preferred: command stays orchestration-only and delegates business work
final class SyncCommand extends Command
{
    public function __construct(private readonly SyncService $syncService)
    {
        parent::__construct();
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $this->syncService->sync((int) $input->getOption('limit'));

        return Command::SUCCESS;
    }
}
```

## Workers and Transports

- On production, prefer CLI workers over the browser-driven admin worker.
- If CLI workers are configured, disable the admin worker explicitly in `config/packages/shopware.yaml`.
- Consume the transports you actually configured. Keep checkout-relevant async work separate from low-priority transport consumption.
- Use `shopware.messenger.routing_overwrite` when a specific Shopware message should be forced onto `low_priority` or another transport without changing the message class.
- Use process supervision such as `systemd` or `supervisor` for long-running workers instead of relying on manual shells.
- Include failed-message inspection and retry commands in operator guidance when the project depends on Messenger.

Example:

```yaml
# config/packages/shopware.yaml
shopware:
  admin_worker:
    enable_admin_worker: false
  messenger:
    routing_overwrite:
      'Your\\Custom\\Message\\RebuildPartnerSnapshotMessage': low_priority
```

```text
Preferred production worker commands:
- bin/console messenger:consume async low_priority --time-limit=60 --memory-limit=512M
- bin/console messenger:failed:show --transport=failed
- bin/console messenger:failed:retry --transport=failed --force
```

## Static Analysis and Quality Gates

- Use the repo's existing quality toolchain first.
- If the project lacks one, prefer PHPStan with Shopware and Symfony-aware configuration, consistent code style tooling, and targeted tests.
- Keep generated resources, migrations, and build output out of the most aggressive analysis paths when that matches the team's setup.

## Local Development and Debugging

- Prefer reproducible local environments over machine-specific assumptions.
- Use targeted profiling and debugging for hot paths instead of leaving verbose debug tooling enabled by default.
- Keep build artifacts, coverage reports, and local editor state out of distributable extension packages.

## CI Behavior

- Run the narrowest checks that prove the change.
- For extension packages, include packaging and validation checks before release when the project uses them.
- Keep quality gates incremental so teams can improve rather than disable tooling wholesale.
- Add sanity checks for duplicate handler registration, container compilation, and command wiring when background jobs or scheduled tasks are involved.

```text
Bad: add a new command and scheduled task but only run php -l on one file.
Good: run the targeted test or command check plus one container-boot or wiring sanity check.
```
