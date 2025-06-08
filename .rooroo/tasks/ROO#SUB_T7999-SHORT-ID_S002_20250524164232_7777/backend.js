const express = require('express');
const db = require('./database_schema');

const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Fridge Inventory Tracking App Backend');
});

// API endpoints
app.get('/items', (req, res) => {
  db.all('SELECT * FROM items', [], (err, rows) => {
    if (err) {
      console.error(err.message);
      res.status(500).send({ error: err.message });
    } else {
      res.json(rows);
    }
  });
});

app.post('/items', (req, res) => {
  const { name, quantity, unit, expiration_date } = req.body;
  db.run(`INSERT INTO items (name, quantity, unit, expiration_date) VALUES (?, ?, ?, ?)`, [name, quantity, unit, expiration_date], function(err) {
    if (err) {
      console.error(err.message);
      res.status(500).send({ error: err.message });
    } else {
      db.get(`SELECT * FROM items WHERE id = ?`, [this.lastID], (err, row) => {
        if (err) {
          console.error(err.message);
          res.status(500).send({ error: err.message });
        } else {
          res.json(row);
        }
      });
    }
  });
});

app.put('/items/:id', (req, res) => {
  const { name, quantity, unit, expiration_date } = req.body;
  const id = req.params.id;
  db.run(`UPDATE items SET name = ?, quantity = ?, unit = ?, expiration_date = ? WHERE id = ?`, [name, quantity, unit, expiration_date, id], function(err) {
    if (err) {
      console.error(err.message);
      res.status(500).send({ error: err.message });
    } else {
      db.get(`SELECT * FROM items WHERE id = ?`, [id], (err, row) => {
        if (err) {
          console.error(err.message);
          res.status(500).send({ error: err.message });
        } else {
          res.json(row);
        }
      });
    }
  });
});

app.delete('/items/:id', (req, res) => {
  const id = req.params.id;
  db.run(`DELETE FROM items WHERE id = ?`, [id], function(err) {
    if (err) {
      console.error(err.message);
      res.status(500).send({ error: err.message });
    } else {
      res.send({ message: 'Deleted' });
    }
  });
});

// Data synchronization
app.get('/backup', (req, res) => {
  db.all('SELECT * FROM items', [], (err, rows) => {
    if (err) {
      console.error(err.message);
      res.status(500).send({ error: err.message });
    } else {
      const fs = require('fs');
      const backupFile = 'inventory_backup.json';
      fs.writeFile(backupFile, JSON.stringify(rows), (err) => {
        if (err) {
          console.error(err.message);
          res.status(500).send({ error: err.message });
        } else {
          res.download(backupFile);
        }
      });
    }
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});