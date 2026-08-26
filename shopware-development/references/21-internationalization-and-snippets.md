# Internationalization and Snippets

## Core Rules

- Keep storefront snippets, admin snippets, and entity translations explicit. Do not mix them into one vague "translations" bucket.
- Use snippets for UI text and translation associations for real entity content.
- Keep language-aware DAL logic aligned with the current context instead of assuming one fallback language or one storefront.
- On 6.7.3+, use base snippet files such as `messages.en.base.json` and keep country-specific files small and intentional.

Example patterns:

```text
Bad: hardcode storefront labels directly in Twig or JS because the first language is English.
Good: use a snippet key and keep the file structure aligned with the plugin's storefront or admin scope.
```

```text
Bad: treat translated entity content like generic customFields and ignore the active language chain.
Good: use proper translation associations and read them in the correct language-aware context.
```

## Storefront and Admin Snippets

- Keep snippet keys namespaced by plugin or feature.
- Do not duplicate the same text across storefront and administration files unless the scopes are truly separate.
- Validate filename and directory conventions when shipping the extension.
- When a translation key changes, update the code and snippet files together.

## Entity Translations

- Use translation associations for content that truly belongs to the entity and changes by language.
- Keep fallback behavior explicit when the current language lacks a value.
- Do not load or persist translated state with the wrong context and then assume storefront rendering will fix it.

## Validation and Release Checks

- For 6.7.3+ translation work, run `bin/console translation:lint-filenames` and `bin/console translation:validate`.
- Check storefront and admin snippet resolution separately when both surfaces changed.
- If the plugin supports 6.6 and 6.7, verify the filename strategy before bulk-renaming snippet files.

## Country-Agnostic Base Snippet Layer (6.7.3+)

Core snippet files renamed for the country-agnostic base layer:

- `en-GB.json` → `en.json`
- `messages.en-GB.base.json` → `messages.en.base.json`

Snippet resolution order:

1. Requested locale (e.g., `en-US`)
2. Country-agnostic base (`en`)
3. Legacy `en-GB`
4. Other fallbacks

Regional variants now hold only ~70 delta snippets instead of ~12,000 duplicates.

- Existing extensions do not need immediate changes; previous naming still resolves.
- New extensions must adopt the country-agnostic naming to be forward-compatible.
- Ship only the diff for `en-US` vs `en`; do not duplicate translations.

Source: developer.shopware.com/docs/resources/references/adr/2025-09-01-adding-a-country-agnostic-language-layer.html.

## Snippet CLI (6.7.11+)

- `bin/console translation:validate` — the current name. `snippets:validate` remains as a deprecated alias slated for removal in 6.8. `snippet:validate` (singular) is not a command; it only ever resolved through Symfony's namespace abbreviation and will stop working.
- `bin/console translation:list`
- `bin/console translation:install --locales it-IT,fr-FR` (interactive multi-select supported)
- `SnippetValidator` becomes `@internal` — do not extend.

Source: release notes 6.7.11.

## Language Pack Sunset In 6.8

The Shopware Language Pack plugin is unsupported from 6.8. Migrate before the jump:

```bash
bin/console translation:install --locales it-IT,fr-FR
```

- Activate every needed language under Settings → Languages before install; inactive languages are ignored.
- Repoint sales-channel domains from `LanguagePack en-US` snippet sets to `BASE en-US`; Language Pack ≥5.37.1 does this automatically.
- If FK constraint errors appear during removal, upgrade to Shopware ≥6.7.7.0 and Language Pack ≥5.37.1 first.

Source: developer.shopware.com/docs/guides/upgrades-migrations/language-pack-migration.html.

## Theme Snippet Keys Required In 6.8

For theme configuration `label` and `helpText`, constructed snippet keys are required in 6.8:

```
sw-theme.<technicalName>.<tabName>.<blockName>.<sectionName>.<fieldName>.label
sw-theme.<technicalName>.<tabName>.<blockName>.<sectionName>.<fieldName>.helpText
```

- API `label` / `helpText` deprecated → `labelSnippetKey` / `helpTextSnippetKey`.
- `ThemeService::getThemeConfiguration()` deprecated → `ThemeConfigurationService::getPlainThemeConfiguration()`.

Full theme details in `17-accessibility-and-template-best-practices.md`.

Source: UPGRADE-6.7.md §6.7.1.0.
