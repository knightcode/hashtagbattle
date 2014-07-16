BEGIN;
CREATE TABLE `hashtag_django_battletag` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tag` varchar(100) NOT NULL,
    `count` integer NOT NULL
)
;
CREATE TABLE `hashtag_django_battle` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `left_hashtag_id` integer NOT NULL,
    `right_hashtag_id` integer NOT NULL
)
;
ALTER TABLE `hashtag_django_battle` ADD CONSTRAINT `left_hashtag_id_refs_id_48e3ae81` FOREIGN KEY (`left_hashtag_id`) REFERENCES `hashtag_django_battletag` (`id`);
ALTER TABLE `hashtag_django_battle` ADD CONSTRAINT `right_hashtag_id_refs_id_48e3ae81` FOREIGN KEY (`right_hashtag_id`) REFERENCES `hashtag_django_battletag` (`id`);

COMMIT;
