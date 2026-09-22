The API expects a Postgres function `match_properties(query_embedding vector(384), match_count int)`
that returns rows with a `property_id` column, ordered by cosine similarity to the query
over a `property_embeddings` table (or wherever embeddings are stored). Example:

```sql
create or replace function match_properties(query_embedding vector(384), match_count int)
returns table (property_id uuid, similarity float)
language sql stable as $$
  select property_id, 1 - (embedding <=> query_embedding) as similarity
  from property_embeddings
  order by embedding <=> query_embedding
  limit match_count;
$$;
```

Adjust the table/column names to match your schema.
