# CMS Elements and Blocks

Index: data model, where slot config really lives, admin registration, inheritance wrappers, previews, custom page types and default layouts, storefront resolvers, rule-based visibility and the HTTP cache, server-side config reads, storefront templates, translating CMS content, layout data vs code, review prompts.

Verified against Shopware 6.7.15 core and admin source unless marked otherwise. Short rules for CMS also live in `12-extension-patterns.md`; this file is the deep reference.

## Data Model

`cms_page` (layout) → `cms_section` → `cms_block` → `cms_slot`. The slot's `type` is the element name. The block's `type` picks the block template.

- **Slot config is translated, all of it.** `CmsSlotDefinition` declares `config` as a `TranslatedField`, stored in `cms_slot_translation.config`. Every setting is per language, not only text: a listing filter switch, slider option, or limit saved in one content language does not apply to another. When a setting "works in English but not in Dutch", check which language's row holds it.
- **Entity overrides sit on the entity, not the layout.** `category_translation`, `product_translation`, and `landing_page_translation` each have `slot_config`, a JSON object keyed by **slot ID**. These are also per language.
- **`cms_page` custom fields are per language too.** `customFields` lives on `CmsPageTranslationDefinition`. If a flag must behave the same in every language, write it only in the system language and show it read-only elsewhere.
- **The Shopping Experiences module never renders custom field sets.** A field set assigned to `cms_page` is invisible in the layout editor until you extend the `sw-cms-sidebar`. Category and landing-page detail pages do render custom field sets, so a per-page flag is often cheaper there.

## How The Storefront Merges Overrides

`SalesChannelCmsPageLoader::overwriteSlotConfig()` starts from the slot's translated layout config and merges the entity override for that slot ID with `overrideArray()`:

- associative arrays merge recursively, key by key
- lists and scalars are replaced whole
- **no key is ever removed**

Consequence: a stale key in an entity override outlives any core rename. In 6.7 the product slider reads `navigationArrows` (`inside` / `outside` / `none`), not the old `navigation` key. A custom template that still reads `navigation` keeps working on any environment whose override row still carries the old key and silently breaks everywhere else. That is the classic "works locally, broken on staging" CMS bug.

## Admin Registration

Register elements and blocks with `Shopware.Service('cmsService').registerCmsElement()` / `registerCmsBlock()`.

Element config keys that matter: `name`, `label`, `component`, `configComponent`, `previewComponent`, `defaultConfig`, `allowedPageTypes`, `disabledConfigInfoTextKey`, `hidden`, `removable`. Block config adds `category`, `previewImage`, and `slots` with per-slot `type` and `default.config`.

`defaultConfig` fields use `{ source, value }` where `source` is `static`, `mapped`, `default`, or `product_stream` (PHP: `FieldConfig::SOURCE_*`). Add `entity: { name, criteria }` when the value holds IDs the editor should load.

```js
// Preferred: element component boots its config through the core mixin
Component.register('sw-cms-el-my-element', {
    template,
    mixins: [Mixin.getByName('cms-element')],
    created() {
        this.initElementConfig('my-element');
    },
});
```

- **Elements with nothing to configure:** set `disabledConfigInfoTextKey` (core does this for `buy-box`, `sidebar-filter`, and others). `sw-cms-slot` then disables the settings button and shows that tooltip. Point the tooltip at where the content comes from, for example a snippet key. Do not ship an empty config panel.
- **Vue 3:** `this.$set` no longer exists. Assign reactive properties directly. Old config components that call it throw when the setting changes.
- **`sw-select-field` is a wrapper around `mt-select` in 6.7** (deprecated for 6.8). It forwards `:options` and drops child `<option>` elements, so a template that writes `<option>` tags renders an empty dropdown. Better: use `mt-select` directly.
- **Event names differ between component families.** `mt-*` fields bind `model-value` and emit `update:model-value`; legacy `sw-*` fields such as `sw-text-editor` bind `value` and emit `update:value`. Core's text element config uses both, behind `METEOR_TEXT_EDITOR`. A listener on the wrong event never fires, so check the component's `emits` when swapping one for the other.

## Inheritance Wrappers (6.7.5+)

Since 6.7.5.0, core wraps every element config field in `<sw-cms-inherit-wrapper>`. It manages one field of `cms_slot_translation.config` versus the content entity's `slot_config`, shows the inherit/override toggle, and restores the layout value on reset.

```twig
{# Preferred: every editable field wrapped, input disabled while inherited #}
<sw-cms-inherit-wrapper
    :element="element"
    field="title"
    :label="$tc('my-plugin.element.title')"
>
    <template #default="{ isInherited }">
        <mt-text-field
            v-model="element.config.title.value"
            :disabled="isInherited"
        />
    </template>
</sw-cms-inherit-wrapper>
```

- Wrap **every** field in a custom element's config component. An unwrapped field gets no inherit/override toggle, so editors can't see whether a page overrides it or reset it to the layout value.
- Put the label on the wrapper (`label` prop), not on the inner input.
- Rich editors need `:key="isInherited"` (core's text element does this) so they re-render when inheritance toggles.
- Disable custom controls inside the wrapper too (date pickers, add/remove buttons). Give reusable sub-components a `disabled` prop.
- `isInherited` is only ever true when a content entity is loaded **and** the admin is not in the system default language. In the system language, edits on a page write straight to the entity's override.
- On 6.6 the wrapper does not exist. Gate it or keep a 6.6 branch.

## Previews And Block Thumbnails

- The 6.7 placeholder image is `assetFilter('/administration/administration/static/img/cms/preview_mountain_small.webp')`. Hardcoded 6.6 paths render a broken image.
- Make the canvas component and block thumbnail resemble the storefront output. Placeholder "Lorem ipsum" previews hide broken config and make editors guess.
- Check that preview SCSS class names match the preview markup. A mismatch leaves the preview unstyled without any error.
- Previews that show snippet text should read it through the snippet API, so admin overrides from Settings > Snippets appear the same as on the storefront.

## Storefront Resolvers

Extend `AbstractCmsElementResolver` (`getType()`, `collect()`, `enrich()`). `CmsElementResolverInterface` is autoconfigured with the `shopware.cms.data_resolver` tag; tag it by hand only when the service is registered without autoconfigure (plain XML service definitions).

- Load everything in `collect()`, attach a struct in `enrich()`, and never query in Twig.
- Return `null` from `collect()` when the slot has nothing to load.
- Resolve **every** field type the element declares. A resolver that only fills `media` fields leaves `mapped` or entity fields empty, and the template renders nothing.
- `mapped` values resolve against the `EntityResolverContext` (product or category page) through `resolveEntityValue()`; `static` values are used as stored; `product_stream` needs the stream's criteria.
- **Associations are not autoloaded.** `product_media.media` is a plain `ManyToOneAssociationField`, so loading product media without `addAssociation('media')` returns rows whose `media` is `null`. A decorated `NavigationRoute` may also drop the category `media` association; load category images separately rather than relying on the tree.
- Sanitize HTML before it reaches the template. Core's `TextCmsElementResolver` runs `HtmlSanitizer` and the template then prints `|raw`. In a custom element, either sanitize in the resolver or use `|sw_sanitize` in Twig. Never `|raw` an unsanitized config value.
- Allowlist values written into `style` or class attributes (for example a colour picker: accept hex, `rgb()`, `hsl()`, fall back otherwise).

## Storefront Templates

- Element templates live at `storefront/element/cms-element-<type>.html.twig`, block templates at `storefront/block/cms-block-<type>.html.twig`. Core includes both with `ignore missing`, so a typo in the name renders nothing without an error.
- Each block's content sits in `.cms-block-container-row.row.cms-row`, a Bootstrap row with negative side margins. A `full-width` section sets the container gutter to `0`, so nothing absorbs those margins and a block whose row is not cancelled out widens the page and causes horizontal scroll. Remove the gutter inside full-width blocks.
- To skip an empty block entirely (no wrapper, no margins), override `storefront/section/cms-section-block-container.html.twig` and test the slot data. An "empty" text slot often contains `<p>&nbsp;</p>`, so trim tags and entities before testing (observed in the 6.7 text editor).
- The layout's `cssClass` lands on the `.cms-page` div, which is a sibling after `.cms-breadcrumb` in `page/content/index.html.twig`. Descendant CSS from the layout class can't reach the breadcrumb; skip the `cms_breadcrumb` block in a Twig override instead.
- Remove `dump()` calls before shipping. They print slot data in dev and fail in production.

## Translating CMS Content

- Text an editor types lives in `cms_slot_translation.config` (layout) and in each entity's `slot_config` override. Text that comes from snippets or data needs no CMS translation.
- Blocks hold no translatable config of their own. Only slots (elements) do.
- Editing text in the layout editor writes `cms_slot_translation`. Saving a category or landing page writes `<entity>_translation.slot_config`. A translation tool that only listens to one of the two misses the other.
- To translate what the visitor actually sees, start from the merged config: layout slot config with the storefront language fallback, plus the entity override. Write back **only the translated fields** into the target language's override. Writing the whole merged config copies every non-text setting and stops later layout changes from reaching that language.
- Skip `mapped` and empty fields. Leave link fields alone unless the URLs are language-specific by design.

## Layout Content Is Data, Not Code

Blocks placed in a layout through the admin, the Admin API, or SQL exist only in that database. They do not travel with a deploy.

- Say so explicitly when you add a block to a local layout for testing.
- Ship plugin-owned default layouts through a migration, with fixed IDs and locked.
- When a block's slot structure changes (for example splitting a title into its own slot), existing layouts and their overrides need a data migration, or the new slot renders empty.

## Review Prompts

- Is every config field in the element's config component inside `<sw-cms-inherit-wrapper>` (6.7.5+), with the input disabled while inherited?
- Does the template read the config keys the current core element uses, or keys from a copied older template?
- Do backend handlers read the effective config (layout plus entity override) rather than the layout alone?
- Does the resolver load every association it renders, and every field type the element declares?
- Is HTML sanitized before `|raw`, and are style/class values allowlisted?
- If visibility depends on rules, is the rule area part of the cache hash when `CACHE_REWORK` is on, and is the page invalidated when only the mapping changes?
- Do previews and thumbnails show what the storefront renders, without broken placeholders?
- Has the user been told which layout changes exist only in the local database?
