# Should-Not-Trigger Prompts

These prompts should NOT auto-invoke the `shopware-development` skill. The description and `paths` field scope the skill to Shopware work. Test in a fresh session; false-positive rate should be ≤ 1/5.

## Generic PHP / Symfony (not Shopware-specific)

1. Set up a plain Symfony 7 application.
2. Debug a PHP 8.4 memory leak in a CLI script.
3. Write a Doctrine ORM migration.
4. Configure Symfony Messenger transports for a generic app.
5. Add PHPStan to a generic PHP project.

## Other e-commerce platforms

6. Fix a Magento 2 plugin bug.
7. Migrate my WooCommerce store to headless.
8. Add a Sylius payment handler.
9. Debug a Prestashop cart calculation.

## Unrelated

10. Refactor my Ruby on Rails app.
11. Explain the difference between k8s deployments and statefulsets.
12. Draft a marketing email for a Black Friday campaign.
13. Write a Terraform module for an S3 bucket.
14. Debug a Node.js websocket disconnect.

## Adjacent but not Shopware

15. Review my Vue 3 application (no Shopware admin context).
16. Set up Pinia in a Nuxt 3 app (no Shopware).
17. Configure Varnish for a plain WordPress site (no Shopware).
18. Migrate my Twig templates from a Symfony 6 app to Symfony 7 (no Shopware).

## Rules

- If any of these auto-invoke, the description or `paths` field is too broad. Tune down.
- If a Shopware prompt fails to trigger, the description is too narrow. Add the missing user paraphrase to `when_to_use`.
