-- Run once in the Supabase SQL editor.
-- 1. Store each review's own feature scores (only features it mentions).
alter table reviews add column if not exists feature_scores jsonb not null default '{}'::jsonb;
alter table reviews add column if not exists created_at timestamptz not null default now();

-- 2. Property-level analysis now records how many reviews mention each feature,
--    and allows NULL when no review mentions it.
alter table analysis
  alter column wifi_score drop not null,
  alter column noise_score drop not null,
  alter column pool_score drop not null,
  alter column food_score drop not null,
  alter column cleanliness_score drop not null,
  alter column location_score drop not null,
  alter column value_score drop not null,
  alter column accessibility_score drop not null,
  add column if not exists wifi_count int not null default 0,
  add column if not exists noise_count int not null default 0,
  add column if not exists pool_count int not null default 0,
  add column if not exists food_count int not null default 0,
  add column if not exists cleanliness_count int not null default 0,
  add column if not exists location_count int not null default 0,
  add column if not exists value_count int not null default 0,
  add column if not exists accessibility_count int not null default 0,
  add column if not exists review_count int not null default 0;

alter table persona_scores
  alter column family_score drop not null,
  alter column business_score drop not null,
  alter column solo_score drop not null,
  alter column accessibility_score drop not null;

-- 3. Upserts need one row per property.
create unique index if not exists analysis_property_id_key on analysis (property_id);
create unique index if not exists persona_scores_property_id_key on persona_scores (property_id);

-- 4. After running this, re-score existing properties from their reviews:
--    python scripts/rescore_all.py   (or POST /api/properties/{id}/recompute per property)
