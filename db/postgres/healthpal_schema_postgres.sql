CREATE TABLE IF NOT EXISTS "user" (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    birthdate DATE NOT NULL,
    gender VARCHAR(40) NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    contact_details VARCHAR(40) NOT NULL,
    nationality VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    location_group VARCHAR(40) NOT NULL,
    school VARCHAR(80) NOT NULL,
    password VARCHAR(40) NOT NULL,
    parent_id INT REFERENCES "user" (user_id) ON DELETE SET NULL,
    role VARCHAR(40) NOT NULL,
    created_date TIMESTAMPTZ NOT NULL,
    last_login TIMESTAMPTZ NOT NULL,
    total_point INT NOT NULL,
    health_tier INT NOT NULL,
    target_minutes INT NOT NULL,
    preferred_intensity INT NOT NULL,
    goal_date DATE NOT NULL
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    title VARCHAR(40) NOT NULL,
    second_title TEXT NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(40) NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    organiser VARCHAR(40) NOT NULL,
    event_type VARCHAR(40) NOT NULL,
    created_date TIMESTAMPTZ NOT NULL,
    max_signups INT NOT NULL,
    current_signups INT NOT NULL,
    mode VARCHAR(40) NOT NULL,
    participant_remark VARCHAR(200) NOT NULL,
    entry_code VARCHAR(40),
    event_point INT NOT NULL,
    event_program VARCHAR(200) NOT NULL,
    tier INT NOT NULL,
    organiser_phone VARCHAR(15) NOT NULL,
    organiser_email VARCHAR(200) NOT NULL
);

CREATE TABLE user_events (
    user_event_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,
    event_id INT NOT NULL REFERENCES events (event_id) ON DELETE CASCADE,
    registered BOOLEAN NOT NULL,
    completed BOOLEAN NOT NULL
);

CREATE TABLE cards (
    card_id SERIAL PRIMARY KEY,
    title VARCHAR(40) NOT NULL,
    collection_id INT NOT NULL,
    points_required INT NOT NULL,
    event_id INT REFERENCES events (event_id) ON DELETE SET NULL,
    description VARCHAR(200) NOT NULL,
    recommendation VARCHAR(300) NOT NULL
);

CREATE TABLE user_cards (
    user_card_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,
    card_id INT NOT NULL REFERENCES cards (card_id) ON DELETE CASCADE,
    earned_date TIMESTAMPTZ NOT NULL
);

CREATE TABLE health (
    health_data_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,
    recorded_date DATE NOT NULL,
    calories INT NOT NULL,
    steps INT NOT NULL,
    sleep_hours FLOAT NOT NULL,
    mvpa_minutes INT NOT NULL,
    calories_per_meal INT NOT NULL
);

CREATE TABLE health_recommendation (
    recommendation_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,
    health_goal VARCHAR(40) NOT NULL,
    recommendation_text TEXT NOT NULL,
    generated_date TIMESTAMPTZ NOT NULL,
    progress VARCHAR(40) NOT NULL
);

CREATE TABLE health_coin (
    points_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,
    points_earned INT NOT NULL,
    earned_date TIMESTAMPTZ NOT NULL,
    source VARCHAR(40) NOT NULL
);

CREATE TABLE performance (
    record_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,
    date TIMESTAMPTZ NOT NULL,
    remark TEXT NOT NULL
);

CREATE TABLE trade (
    trade_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,
    card_one_id INT NOT NULL,
    card_two_id INT NOT NULL,
    trade_date TIMESTAMPTZ NOT NULL
);

CREATE TABLE goal (
    goal_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "user" (user_id) ON DELETE CASCADE,
    goal_description VARCHAR(256) NOT NULL,
    tier INT NOT NULL,
    date_created TIMESTAMPTZ NOT NULL,
    target INT NOT NULL
);

CREATE TABLE streak (
    streak_id SERIAL PRIMARY KEY,
    goal_id INT NOT NULL REFERENCES goal (goal_id) ON DELETE CASCADE,
    week_started INT NOT NULL,
    week_current INT NOT NULL,
    streak_count INT NOT NULL DEFAULT 0
);

CREATE TABLE strava_users (
    id SERIAL PRIMARY KEY,
    strava_id VARCHAR(50) UNIQUE,
    access_token VARCHAR(200) NOT NULL,
    refresh_token VARCHAR(200) NOT NULL,
    expires_at INT NOT NULL
);

CREATE TABLE collection (
    collection_id SERIAL PRIMARY KEY,
    collection_name VARCHAR(50) NOT NULL,
    expired TIMESTAMPTZ
);
