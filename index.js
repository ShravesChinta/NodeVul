const express = require('express');
const request = require('request'); // DEPRECATED
const chalk = require('chalk');
const moment = require('moment');   // HEAVY
const _ = require('lodash');
const download = require('download');
const fs = require('fs');

const app = express();

app.get('/feed', async (req, res) => {
  request('https://jsonplaceholder.typicode.com/posts?_limit=3', async (err, _, body) => {
    const posts = JSON.parse(body);
    for (let i = 0; i < posts.length; i++) {
      const imagePath = `./images/post-${i}.jpg`;
      await download('https://picsum.photos/200')
        .pipe(fs.createWriteStream(imagePath));
      posts[i].image = imagePath;
    }
    res.send(posts);
  });
});

app.listen(3000, () => {
  console.log(chalk.green(`Started at ${moment().format()}`));
});
