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
    return "ERROR";
  }


  const seasons =
    response.results[0].properties.Season.multi_select;


  if (seasons.length !== 1) {
    return "ERROR";
  }


  return seasons[0].name;
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

  const currentSeason = await findCurrentSeason();


  let previousSeason = "";

  if (fs.existsSync(LAST_SEASON_FILE)) {

    previousSeason =
      fs.readFileSync(
        LAST_SEASON_FILE,
        "utf8"
      ).trim();

  }


  console.log("Current:", currentSeason);
  console.log("Previous:", previousSeason);


  if (currentSeason === previousSeason) {

    console.log(
      "No season change. Skipping update."
    );

    return;

  }


  const image =
    seasonImages[currentSeason] ||
    seasonImages.ERROR;


  await updateImage(image);


  fs.writeFileSync(
    LAST_SEASON_FILE,
    currentSeason
  );


  console.log(
    "Season updated to:",
    currentSeason
  );

}


main();
