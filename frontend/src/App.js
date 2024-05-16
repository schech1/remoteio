import React from 'react';
import RemoteIO from './RemoteIO'; // Import the RemoteIO component

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Remote IO Control</h1>
      </header>
      <main>
        <RemoteIO /> {/* Render the RemoteIO component */}
      </main>
    </div>
  );
}

export default App;
