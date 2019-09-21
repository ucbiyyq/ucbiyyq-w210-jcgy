# basic eda on data
#
library(tidyverse)
library(janitor)
library(here)
library(repurrrsive)
library(xml2)

# eda of stackoverflow tags -------------------------
#
stackoverflow_tags %>% colnames() # id, tag_name, count, excerpt_post_id, wiki_post_id 
stackoverflow_tags %>% nrow() # 55665 rows
stackoverflow_tags %>% distinct(tag_name) %>% nrow() # 55665
stackoverflow_tags %>% select(id, count, excerpt_post_id, wiki_post_id) %>% summary()

# ... counts of is.na
stackoverflow_tags %>% 
    map_df(is.na) %>% 
    pivot_longer(everything()) %>% 
    count(name, value) %>% 
    rename(is_na = value) %>% 
    pivot_wider(names_from = is_na, values_from = n, values_fill = list(n = 0))
# ... looks like we have about 25% of tags without post ids ???

# ... checks for dups
assert_that(stackoverflow_tags %>% count(id, sort = TRUE) %>% filter(n > 1) %>% nrow() == 0) # no dups of id
assert_that(stackoverflow_tags %>% count(tag_name, sort = TRUE) %>% filter(n > 1) %>% nrow() == 0) # 0, no dups of tagnames
assert_that(stackoverflow_tags %>% count(excerpt_post_id, sort = TRUE) %>% filter(n > 1 & !is.na(excerpt_post_id)) %>% nrow() == 0) # not counting the NA posts, no dups
assert_that(stackoverflow_tags %>% count(wiki_post_id, sort = TRUE) %>% filter(n > 1 & !is.na(wiki_post_id)) %>%  nrow() == 0) # not counting the NA posts, no dups

# ... top tags
stackoverflow_tags %>% 
    select(tag_name, count) %>% 
    top_n(n = 20, wt = count) %>% 
    ggplot(aes(reorder(tag_name, count), count)) + 
    geom_col() +
    coord_flip()
