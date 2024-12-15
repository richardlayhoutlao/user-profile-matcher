INSERT INTO campaigns (
    campaign_id,
    game,
    name,
    priority,
    matchers,
    start_date,
    end_date,
    enabled,
    last_updated
) VALUES (
    'b1f9e5d4-8af4-4e7e-9e57-74db7c4b3e2c', 
    'mygame',
    'mycampaign',
    10.5,
    '{
        "level": {
            "min": 1,
            "max": 3
        },
        "has": {
            "country": ["US", "RO", "CA"],
            "items": ["item_1"]
        },
        "does_not_have": {
            "items": ["item_4"]
        }
    }',
    '2022-01-25T00:00:00Z',
    '2022-02-25T00:00:00Z',
    1, -- SQLite uses 1 for true
    '2021-07-13T11:46:58Z'
);

INSERT INTO campaigns (
    campaign_id,
    game,
    name,
    priority,
    matchers,
    start_date,
    end_date,
    enabled,
    last_updated
) VALUES (
    'z1f9e5d4-8af4-4e7e-9e57-74db7c4b3e87',
    'mygame2020-2025',
    'mycampaign2020-2025',
    10.5,
    '{
        "level": {
            "min": 1,
            "max": 3
        },
        "has": {
            "country": ["US", "RO", "CA"],
            "items": ["item_1"]
        },
        "does_not_have": {
            "items": ["item_4"]
        }
    }',
    '2020-01-25T00:00:00Z',
    '2027-02-25T00:00:00Z',
    1, -- SQLite uses 1 for true
    '2021-07-13T11:46:58Z'
);
