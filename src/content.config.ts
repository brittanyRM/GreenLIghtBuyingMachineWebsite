import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

/* Every block type the page renderer knows how to draw.
   Adding a type here means adding a case in <Blocks /> and an entry
   in public/admin/config.yml — all three stay in step. */
const block = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("prose"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    columns: z.array(z.object({ body: z.string() })).optional(),
    body: z.string().optional(),
  }),
  z.object({
    type: z.literal("stats"),
    items: z.array(z.object({ value: z.string(), label: z.string() })),
  }),
  z.object({
    type: z.literal("roles"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    items: z.array(
      z.object({ kicker: z.string(), title: z.string(), body: z.string() }),
    ),
  }),
  z.object({
    type: z.literal("fit"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    fitTitle: z.string().default("A fit if you"),
    fit: z.array(z.string()),
    notTitle: z.string().default("Not a fit if you"),
    not: z.array(z.string()),
  }),
  z.object({
    type: z.literal("stages"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    items: z.array(z.object({ title: z.string(), body: z.string() })),
  }),
  z.object({
    type: z.literal("qa"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    items: z.array(z.object({ question: z.string(), answer: z.string() })),
  }),
  z.object({
    type: z.literal("lists"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    left: z.array(z.string()),
    right: z.array(z.string()),
    footnote: z.string().optional(),
  }),
  z.object({
    type: z.literal("gallery"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    set: z.enum(["homes", "plans"]),
    limit: z.number().optional(),
  }),
  z.object({
    type: z.literal("doors"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    items: z.array(
      z.object({
        kicker: z.string(),
        title: z.string(),
        body: z.string(),
        note: z.string().optional(),
        ctaLabel: z.string(),
        ctaHref: z.string(),
        accent: z.enum(["build", "buy"]).default("build"),
      }),
    ),
  }),
  z.object({
    type: z.literal("callout"),
    kicker: z.string().optional(),
    heading: z.string().optional(),
    body: z.string(),
  }),
  z.object({
    type: z.literal("cta"),
    heading: z.string(),
    body: z.string().optional(),
    primaryLabel: z.string().optional(),
    primaryHref: z.string().optional(),
    secondaryLabel: z.string().optional(),
    secondaryHref: z.string().optional(),
  }),
  z.object({
    type: z.literal("form"),
    heading: z.string().optional(),
    lede: z.string().optional(),
    form: z.enum(["apply", "property", "prequal", "book"]),
    aside: z.string().optional(),
  }),
  z.object({
    type: z.literal("people"),
    heading: z.string().optional(),
    body: z.string(),
  }),
  z.object({
    type: z.literal("html"),
    body: z.string(),
  }),
]);

const pages = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/pages" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    kicker: z.string().optional(),
    heading: z.string(),
    lede: z.string().optional(),
    navLabel: z.string().optional(),
    order: z.number().optional(),
    hidden: z.boolean().default(false),
    noindex: z.boolean().default(false),
    blocks: z.array(block).default([]),
  }),
});

const settings = defineCollection({
  loader: glob({ pattern: "site.json", base: "./src/content/settings" }),
  schema: z.object({
    brand: z.string(),
    tagline: z.string(),
    email: z.string(),
    phone: z.string(),
    phoneHref: z.string(),
    instagram: z.string().optional(),
    youtube: z.string().optional(),
    trinity: z.string().optional(),
    ga4: z.string().optional(),
    navCtaPrimary: z.object({ label: z.string(), href: z.string() }),
    navCtaSecondary: z.object({ label: z.string(), href: z.string() }),
    footerFinePrint: z.string(),
  }),
});

export const collections = { pages, settings };
