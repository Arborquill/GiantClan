require("dotenv").config();

const { Client } = require("@notionhq/client");
const fs = require("fs");

const notion = new Client({
  auth: process.env.NOTION_TOKEN,
});


// ================================
// CONFIG
// ================================

const DATABASE_ID = "bf29cd66-e972-82c2-903f-0707b15b4bf3";

const IMAGE_BLOCK_ID = "3af9cd66-e972-8108-9e1f-d620bde59c95";

const LAST_SEASON_FILE = "last-season.txt";


// GitHub hosted images
const seasonImages = {

  "Newleaf":
    "https://raw.githubusercontent.com/Arborquill/GiantClan/main/Newleaf.png",

  "Greenleaf":
    "https://raw.githubusercontent.com/Arborquill/GiantClan/main/Greenleaf.png",

  "Leaf-fall":
    "https://raw.githubusercontent.com/Arborquill/GiantClan/main/Leaf-fall.png",

  "Leaf-bare":
    "https://raw.githubusercontent.com/Arborquill/GiantClan/main/Leaf-bare.png",

  "ERROR":
    "https://raw.githubusercontent.com/Arborquill/GiantClan/main/Camp_error.png",

};


// ================================
// FIND REFRESH REQUEST
// ================================

async function findRefreshRequest() {

  const response = await notion.dataSources.query({

    data_source_id: DATABASE_ID,

    filter: {
      property: "Refresh Image",
      checkbox: {
        equals: true,
      },
    },

  });


  if (response.results.length === 0) {

    return null;

  }


  return response.results[0];

}


// ================================
// CLEAR REFRESH CHECKBOX
// ================================

async function clearRefreshRequest(pageId) {

  await notion.pages.update({

    page_id: pageId,

    properties: {

      "Refresh Image": {
        checkbox: false,
      },

    },

  });

}


// ================================
// FIND CURRENT SEASON
// ================================

async function findCurrentSeason() {

  const response = await notion.dataSources.query({

    data_source_id: DATABASE_ID,

    filter: {

      property: "Played",

      checkbox: {
        equals: true,
      },

    },

    sorts: [

      {
        property: "Date",
        direction: "descending",
      },

    ],

    page_size: 1,

  });


  if (response.results.length === 0) {

    console.log(
      "No played seasons found."
    );

    return "ERROR";

  }


  const page = response.results[0];


  const seasons =
    page.properties.Season.multi_select;


  console.log(
    "Latest played:",
    page.properties.Name.title[0]?.plain_text
  );


  console.log(
    "Seasons:",
    seasons.map(s => s.name)
  );


  if (seasons.length !== 1) {

    console.log(
      "Invalid season count."
    );

    return "ERROR";

  }


  return seasons[0].name;

}


// ================================
// LAST SEASON MEMORY
// ================================

function getLastSeason() {

  if (!fs.existsSync(LAST_SEASON_FILE)) {

    return "";

  }


  return fs
    .readFileSync(
      LAST_SEASON_FILE,
      "utf8"
    )
    .trim();

}


function saveLastSeason(season) {

  fs.writeFileSync(
    LAST_SEASON_FILE,
    season
  );

}


// ================================
// UPDATE IMAGE
// ================================

async function updateImage(imageUrl) {

  await notion.blocks.update({

    block_id: IMAGE_BLOCK_ID,

    image: {

      external: {
        url: imageUrl,
      },

    },

  });

}


// ================================
// MAIN
// ================================

async function main() {

  try {

    const refreshRequest =
      await findRefreshRequest();


    const forceUpdate =
      refreshRequest !== null;


    const currentSeason =
      await findCurrentSeason();


    const previousSeason =
      getLastSeason();


    console.log(
      "Current season:",
      currentSeason
    );


    console.log(
      "Previous season:",
      previousSeason
    );


    console.log(
      "Force update:",
      forceUpdate
    );


    if (
      currentSeason === previousSeason &&
      currentSeason !== "ERROR" &&
      !forceUpdate
    ) {

      console.log(
        "No season change. Skipping update."
      );

      return;

    }


    const image =
      seasonImages[currentSeason] ||
      seasonImages.ERROR;


    console.log(
      "Updating image:"
    );

    console.log(
      image
    );


    await updateImage(image);


    if (currentSeason !== "ERROR") {

      saveLastSeason(
        currentSeason
      );

    }


    if (forceUpdate) {

      await clearRefreshRequest(
        refreshRequest.id
      );

      console.log(
        "Refresh checkbox cleared."
      );

    }


    console.log(
      "Image update complete."
    );


  } catch (error) {

    console.error(
      "ERROR:"
    );

    console.error(
      error.message
    );

    process.exit(1);

  }

}


main();
