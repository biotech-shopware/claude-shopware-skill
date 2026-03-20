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

- For 6.7.3+ translation work, run `translation:lint-filenames` and `snippet:validate` where available.
- Check storefront and admin snippet resolution separately when both surfaces changed.
- If the plugin supports 6.6 and 6.7, verify the filename strategy before bulk-renaming snippet files.
