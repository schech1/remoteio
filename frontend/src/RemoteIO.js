import React, { useState } from 'react';
import axios from 'axios';
import { Box, Button, TextField, Typography, Container, Paper, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton } from '@mui/material';
import { AddCircleOutline, Delete } from '@mui/icons-material';
import { Snackbar, Alert } from '@mui/material';


const RemoteIO = () => {
  const [hosts, setHosts] = useState([]);
  const [customHost, setCustomHost] = useState('');
  const [customPort, setCustomPort] = useState('');
  const [selectedHost, setSelectedHost] = useState(null);
  const [selectedPin, setSelectedPin] = useState(null);
  const [timeMs, setTimeMs] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  
  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };
  
  const handleAddCustomHost = () => {
    if (customHost && customPort) {
      setHosts([...hosts, { host: customHost, port: customPort }]);
      setCustomHost('');
      setCustomPort('');
    }
  };
  

  const handleRemoveHost = (index) => {
    const updatedHosts = [...hosts];
    updatedHosts.splice(index, 1);
    setHosts(updatedHosts);
    if (selectedHost === index) {
      setSelectedHost(null);
    }
  };

  const handlePinAction = async (action) => {
    if (selectedHost === null || typeof selectedHost === 'undefined' || selectedHost < 0 || selectedHost >= hosts.length) {
      setSnackbarMessage('No valid host selected');
      setSnackbarOpen(true);
      return;
    }
  
    try {
      const response = await axios.post(`${hosts[selectedHost].host}:${hosts[selectedHost].port}/pin/${selectedPin}/${action}`, {
        time_ms: timeMs,
      });
      setStatusMessage(`Action ${action} on pin ${selectedPin} was successful`);
    } catch (error) {
      console.error(`Error performing action ${action} on pin ${selectedPin}:`, error);
      setStatusMessage(`Error performing action ${action} on pin ${selectedPin}`);
    }
    const summaryMessage = `Action ${action} on pin ${selectedPin} at ${hosts[selectedHost].host} for ${timeMs} ms`;
    setSnackbarMessage(summaryMessage);
    setSnackbarOpen(true);
  };
  
  

  const handlePinSelect = (pin) => {
    setSelectedPin(pin === selectedPin ? null : pin);
  };

  const handlePresetTime = (time) => {
    setTimeMs(time);
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '2rem' }}>
      <Paper elevation={3} style={{ padding: '2rem' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Remote IO Control
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
          <TextField
            id="custom-host"
            label="Custom Host"
            value={customHost}
            onChange={(e) => setCustomHost(e.target.value)}
            variant="outlined"
            sx={{ mr: 1 }}
          />
          <TextField
            id="custom-port"
            label="Custom Port"
            type="number"
            value={customPort}
            onChange={(e) => setCustomPort(e.target.value)}
            variant="outlined"
            sx={{ mr: 1 }}
          />
          <Button variant="contained" onClick={handleAddCustomHost} startIcon={<AddCircleOutline />}>
            Add Host
          </Button>
        </Box>
        <List>
          {hosts.map((host, index) => (
            <ListItem key={index} button selected={selectedHost === index} onClick={() => setSelectedHost(index)}>
              <ListItemText primary={`${host.host}:${host.port}`} />
              <ListItemSecondaryAction>
                <IconButton edge="end" onClick={() => handleRemoveHost(index)}>
                  <Delete />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '2rem', overflowX: 'auto' }}>
          {[...Array(10)].map((_, index) => (
            <Button
              key={index}
              variant={selectedPin === index ? 'contained' : 'outlined'}
              color="primary"
              style={{ margin: '0.5rem', minWidth: '40px' }}
              onClick={() => handlePinSelect(index)}
            >
              {index}
            </Button>
          ))}
        </div>
        <Box component="form" noValidate autoComplete="off" sx={{ '& .MuiTextField-root': { m: 1, width: '25ch' }, }}>
          <TextField
            id="time-ms"
            label="Custom Time (ms)"
            type="number"
            value={timeMs}
            onChange={(e) => setTimeMs(e.target.value)}
            variant="outlined"
          />
          <Box sx={{ '& button': { m: 1, }, }}>
            <Button variant="contained" onClick={() => handlePresetTime(100)}>100ms</Button>
            <Button variant="contained" onClick={() => handlePresetTime(1000)}>1 sec</Button>
            <Button variant="contained" onClick={() => handlePresetTime(10000)}>10 sec</Button>
          </Box>
        </Box>
        <Box sx={{ '& button': { m: 1 } }}>
  <Button
    variant="contained"
    color="primary"
    onClick={() => handlePinAction('on')}
    disabled={selectedPin === null || timeMs === ''}
  >
    On
  </Button>
  <Button
    variant="contained"
    color="secondary"
    onClick={() => handlePinAction('off')}
    disabled={selectedPin === null || timeMs === ''}
  >
    Off
  </Button>
  <Button
    variant="contained"
    color="info"
    onClick={() => handlePinAction('blink')}
    disabled={selectedPin === null || timeMs === ''}
  >
    Blink
  </Button>
  <Button
    variant="contained"
    color="success"
    onClick={() => handlePinAction('pulse')}
    disabled={selectedPin === null || timeMs === ''}
  >
    Pulse
  </Button>
</Box>

<Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={handleSnackbarClose}>
    <Alert onClose={handleSnackbarClose} severity="success" sx={{ width: '100%' }}>
      {snackbarMessage}
    </Alert>
  </Snackbar>

        {statusMessage && (
          <Typography variant="body1" color="textPrimary" style={{ marginTop: '1rem' }}>
            {statusMessage}
          </Typography>
        )}
      </Paper>
    </Container>
  );
  
};

export default RemoteIO;

