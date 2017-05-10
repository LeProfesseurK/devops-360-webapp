CREATE TABLE IF NOT EXISTS battle (
    battle_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,

    beer_win_id SMALLINT UNSIGNED NOT NULL,
    beer_lose_id SMALLINT UNSIGNED NOT NULL,
    beer_win_rate TINYINT SIGNED NOT NULL,

    CONSTRAINT fk_beer_win_id FOREIGN KEY (beer_win_id) REFERENCES beer (id),
    CONSTRAINT fk_beer_lose_id FOREIGN KEY (beer_lose_id) REFERENCES beer (id),
    CONSTRAINT pk_beer_battle_id PRIMARY KEY (battle_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
