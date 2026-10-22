IF DB_ID('HotelsDb') IS NULL CREATE DATABASE HotelsDb;
GO
USE HotelsDb;
GO
IF OBJECT_ID('dbo.Hotels') IS NOT NULL DROP TABLE dbo.Hotels;
CREATE TABLE dbo.Hotels (
    HotelId        INT IDENTITY(1,1) PRIMARY KEY,
    HotelName      NVARCHAR(100) NOT NULL,
    City           NVARCHAR(60)  NOT NULL,
    Country        NVARCHAR(60)  NOT NULL,
    Category       NVARCHAR(40)  NOT NULL,
    Rating         DECIMAL(2,1)  NOT NULL,
    PricePerNight  DECIMAL(8,2)  NOT NULL,
    ParkingIncluded BIT          NOT NULL,
    Tags           NVARCHAR(200) NULL,
    Description    NVARCHAR(1000) NOT NULL
);
INSERT INTO dbo.Hotels (HotelName, City, Country, Category, Rating, PricePerNight, ParkingIncluded, Tags, Description) VALUES
(N'Sunset Beach Resort', N'Miami', N'USA', N'Resort', 4.6, 289.00, 1, N'beach,pool,spa', N'Oceanfront resort with a private beach, infinity pool and full-service spa. Quiet mornings, lively sunset bar.'),
(N'Harbor Light Inn', N'Boston', N'USA', N'Boutique', 4.4, 215.00, 0, N'historic,waterfront', N'Cozy boutique inn in a restored 1890s building overlooking the harbor. Fireplace lounge and fresh pastries every morning.'),
(N'Alpine Chalet Lodge', N'Zermatt', N'Switzerland', N'Lodge', 4.8, 410.00, 1, N'ski,mountain,fireplace', N'Wood-panelled chalet steps from the ski lift with panoramic Matterhorn views, sauna and a hearty breakfast.'),
(N'Metro Business Hotel', N'Chicago', N'USA', N'Business', 4.1, 169.00, 1, N'business,wifi,gym', N'Modern downtown hotel with fast Wi-Fi, 24-hour gym and meeting rooms. Five minutes from the train station.'),
(N'Desert Mirage Resort', N'Phoenix', N'USA', N'Resort', 4.3, 199.00, 1, N'pool,golf,desert', N'Sprawling desert resort with three pools, a championship golf course and sunset views over the mountains.'),
(N'Old Town Guesthouse', N'Prague', N'Czech Republic', N'Budget', 3.9, 62.00, 0, N'budget,historic,central', N'Friendly family-run guesthouse in the heart of the old town. Simple clean rooms, walkable to all landmarks.'),
(N'Lagoon Overwater Villas', N'Male', N'Maldives', N'Luxury', 4.9, 780.00, 0, N'beach,overwater,romantic', N'Private overwater villas with glass floors, direct lagoon access and a world-class dive centre. Ideal for honeymoons.'),
(N'Capital Plaza Hotel', N'Washington', N'USA', N'Business', 4.0, 185.00, 1, N'business,central', N'Classic full-service hotel near the museums and government district with a grand ballroom and executive lounge.'),
(N'Lakeview Retreat', N'Lake Tahoe', N'USA', N'Lodge', 4.5, 245.00, 1, N'lake,hiking,quiet', N'Peaceful lakeside lodge with hiking trails, kayaks and a stone fireplace. A quiet escape for nature lovers.'),
(N'Neon District Hostel', N'Tokyo', N'Japan', N'Hostel', 4.2, 38.00, 0, N'budget,social,central', N'Lively hostel with capsule beds, a shared kitchen and a rooftop terrace. Great for solo travelers on a budget.'),
(N'Riad Al Jasmin', N'Marrakech', N'Morocco', N'Boutique', 4.7, 135.00, 0, N'courtyard,spa,historic', N'Traditional riad with a tiled courtyard, rooftop terrace and hammam. Authentic, intimate and beautifully quiet.'),
(N'Skyline Tower Hotel', N'Dubai', N'UAE', N'Luxury', 4.7, 520.00, 1, N'luxury,skyline,pool', N'Ultra-modern tower hotel with a sky-high infinity pool, fine dining and floor-to-ceiling city views.'),
(N'Vineyard Country Inn', N'Napa', N'USA', N'Boutique', 4.6, 330.00, 1, N'wine,romantic,quiet', N'Romantic inn surrounded by vineyards, offering wine tastings, a farm-to-table restaurant and garden suites.'),
(N'Airport Express Stay', N'Frankfurt', N'Germany', N'Budget', 3.6, 89.00, 1, N'airport,shuttle,budget', N'No-frills hotel with a free airport shuttle and soundproofed rooms. Perfect for early flights and layovers.'),
(N'Coral Bay Family Resort', N'Cancun', N'Mexico', N'Resort', 4.4, 265.00, 1, N'beach,family,kids-club', N'All-inclusive family resort with a kids club, water park and calm shallow bay ideal for children.'),
(N'Highland Castle Hotel', N'Edinburgh', N'UK', N'Historic', 4.5, 240.00, 0, N'castle,historic,whisky', N'Converted castle with turrets, a whisky bar and tartan-clad rooms, a short walk from the Royal Mile.'),
(N'Greenleaf Eco Lodge', N'Monteverde', N'Costa Rica', N'Lodge', 4.7, 155.00, 0, N'eco,wildlife,hiking', N'Solar-powered eco lodge in the cloud forest. Guided wildlife walks, organic meals and hummingbird gardens.'),
(N'Central Park South Suites', N'New York', N'USA', N'Luxury', 4.5, 610.00, 0, N'luxury,central,city', N'Elegant all-suite hotel facing Central Park with concierge service and a refined afternoon tea.'),
(N'Sakura Ryokan', N'Kyoto', N'Japan', N'Boutique', 4.8, 290.00, 0, N'onsen,traditional,quiet', N'Traditional ryokan with tatami rooms, private onsen baths and multi-course kaiseki dinners. Deeply tranquil.'),
(N'Bondi Surf Hotel', N'Sydney', N'Australia', N'Budget', 4.0, 120.00, 0, N'beach,surf,social', N'Relaxed hotel a minute from Bondi Beach with surfboard rental and a casual rooftop bar.');
GO
