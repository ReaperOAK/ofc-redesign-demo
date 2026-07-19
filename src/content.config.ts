import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";

const services = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/services" }),
  schema: z.object({
    title: z.string(),
    order: z.number(),
    summary: z.string(),
    capabilities: z.array(z.string()).min(1),
  }),
});

const caseStudies = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/case-studies" }),
  schema: z.object({
    title: z.string(),
    sector: z.string(),
    order: z.number(),
    metric: z.string().nullable(),
    metricLabel: z.string().nullable(),
    summary: z.string(),
  }),
});

export const collections = { services, caseStudies };
