# NewTweather
Revamped Tweather (cleaner)

Tweather aggregates local Twitter data based on geotagging to provide a more human-centric picture of what the weather's like.
Have you ever wondered what does 0F, 40F, 80F, or 100F really mean in terms of actions and emotion?
By providing a visualization of recent tweets in your area we can show you what people are actually describing the weather as.
Maybe it's "Bro the the weather is down in the dumpsters, get out! #bad", or "Not just sweater weather, fingers freezing wear
your gloves and scarves #frigid", these descriptions by actual people in the weather let us know what we should be doing.

Using the Google maps API, we can visualize the tweets sourcing them to wear they come from and let you know what areas might have
different conditions. Using TwitterSearch https://github.com/ckoepp/TwitterSearch, we collect tweets and analyze them for what kind
of weather the tweets are describing. With flask/HTML/Javascript we send the server side processing of tweets to create a dynamic webpage.

