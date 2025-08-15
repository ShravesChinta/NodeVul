import express from 'express';
import axios from 'axios';
import chalk from 'chalk';
import dayjs from 'dayjs';
import fetch from 'node-fetch';
import fs from 'fs';
import { pipeline } from 'stream';
import { promisify } from 'util';

const streamPipeline = promisify(pipeline);
const app = express();

app.get('/feed', async (req, res) => {
  try {
    const response = await axios.get('https://jsonplaceholder.typicode.com/posts?_limit=3');
    const posts = response.data;

    for (let i = 0; i < posts.length; i++) {
      const imgRes = await fetch('https://picsum.photos/200');
      const dest = fs.createWriteStream(`./images/post-${i}.jpg`);
      await streamPipeline(imgRes.body, dest);
      posts[i].image = `post-${i}.jpg`;
    }

    res.send(posts);
  } catch (err) {
    res.status(500).send('Error fetching feed');
  }
});

app.listen(3000, () => {
  console.log(chalk.green(`Server started at ${dayjs().format('YYYY-MM-DD HH:mm:ss')}`));
});
