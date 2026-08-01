require("dotenv").config();

const { Client } = require("@notionhq/client");

const notion = new Client({
  auth: process.env.NOTION_TOKEN,
});


// ================================
// CONFIG
// ================================

// Archive database data source ID
const DATABASE_ID = "bf29cd66-e972-82c2-903f-0707b15b4bf3";

// GiantClan Camp image block
const IMAGE_BLOCK_ID = "3af9cd66-e972-8108-9e1f-d620bde59c95";


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
    console.log("No played seasons found.");
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


  // Must have exactly one season
  if (seasons.length !== 1) {

    console.log(
      "Invalid season count. Using error image."
    );

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

  try {

    const season = await findCurrentSeason();


    console.log(
      "Current season:",
      season
    );


    const image =
      seasonImages[season] ||
      seasonImages.ERROR;


    console.log(
      "Updating image:"
    );

    console.log(image);


    await updateImage(image);


    console.log(
      "Image updated successfully!"
    );


  } catch (error) {

    console.error(
      "ERROR:"
    );

    console.error(
      error.message
    );

  }

}


main();