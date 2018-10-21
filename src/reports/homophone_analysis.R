library(tidyverse)
library(lme4)


setwd("/Users/seantrott/Dropbox/UCSD/Research/Systematicity/homophones")
dat = read_csv("data/processed/wordpair_comparisons.csv")

multiple_spellings = read_csv("data/hand_annotated/multiple_spellings.csv")
alternates = c(multiple_spellings$w1, multiple_spellings$w2)

dat = dat %>%
  filter((w1 %in% alternates)==FALSE &
           (w2 %in% alternates)==FALSE)

dat %>%
  ggplot(aes(x = meaning_distance,
             fill = factor(phonetic_distance))) +
  geom_density(alpha = .6) +
  theme_minimal() + 
  facet_grid(~phonetic_distance)


### Descriptive
mean(filter(dat, is_homophone=="True")$meaning_distance)
sd(filter(dat, is_homophone=="True")$meaning_distance)
mean(filter(dat, is_homophone=="False")$meaning_distance)
sd(filter(dat, is_homophone=="False")$meaning_distance)

dat %>%
  ggplot(aes(x = phonetic_distance,
             y = meaning_distance,
             color = same_class)) +
  geom_point(alpha = .6) +
  geom_smooth(method = "lm") +
  theme_minimal()

### Models 
model_all = lmer(data=monomorphemes,
                 meaning_distance ~ phonetic_distance + is_homophone + same_class + high_freq + low_freq + long_length + short_length +
            (1 | w1) + (1 | w2),
          REML=FALSE)

m1.homophone = lmer(data=monomorphemes,
                    meaning_distance ~ is_homophone + (1 | w1) + (1 | w2),
                    REML=FALSE)
m1.form = lmer(data=monomorphemes,
               meaning_distance ~ phonetic_distance + (1 | w1) + (1 | w2),
               REML=FALSE)
m1.null= lmer(data=monomorphemes,
              meaning_distance ~ (1 | w1) + (1 | w2),
              REML=FALSE)

simple_lm = lm(data=dat,
               meaning_distance ~ phonetic_distance + high_freq + low_freq +
                 same_class + is_homophone + orthographic_neighborhood_w1 + orthographic_neighborhood_w2)


binned = dat %>% group_by(phonetic_distance, same_class) %>% summarise(mean_meaning = mean(meaning_distance),
                                                          sd_meaning = sd(meaning_distance),
                                                          se_meaning = sd(meaning_distance)/sqrt(nrow(dat)))

binned %>%
  # filter(phonetic_distance > 0) %>%
  ggplot(aes(x = phonetic_distance,
             y = mean_meaning,
             color = same_class)) +
  geom_line(stat = "identity") +
  geom_errorbar(aes(ymin = mean_meaning - 4*se_meaning,
                    ymax = mean_meaning + 4*se_meaning,
                    width = .1)) +
  labs(x = "Form distance",
       y = "Meaning similarity",
       title = "Meaning similarity by form distance") +
  theme_minimal()


summary(lm(data=filter(dat, same_class=="False"),
           meaning_distance ~ is_homophone))

