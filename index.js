// index.js
const express = require('express');
const request = require('request');
const _ = require('lodash');
const moment = require('moment');

const app = express();

app.get('/', (req, res) => {
  const now = moment().format('MMMM Do YYYY, h:mm:ss a');
  request('https://jsonplaceholder.typicode.com/posts/1', (err, response, body) => {
    if (err) {
      res.status(500).send('Error occurred');
    } else {
      const data = JSON.parse(body);
      if (_.isEmpty(data)) {
        res.send('Empty response');
      } else {
        res.send(`At ${now}, fetched post: ${data.title}`);
      }
    }
  });
});

app.listen(3000, () => console.log('Listening on port 3000'));
