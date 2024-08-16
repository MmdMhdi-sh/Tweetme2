import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { TweetsComponent } from './tweets';
import reportWebVitals from './reportWebVitals';


const appEl = document.getElementById('root')
if (appEl) {
  const root = ReactDOM.createRoot(appEl);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}

// .dataset gives you the properties of the element starting with 'data-'. Ex. data-username='username' => {username:"username"}
const tweetsEl = document.getElementById('tweetme-2')
const e = React.createElement
if (tweetsEl) {
  const root = ReactDOM.createRoot(tweetsEl);
  root.render(e(TweetsComponent, tweetsEl.dataset));
  // root.render(
  //   <React.StrictMode>
  //     <TweetsComponent username={tweetsEl.dataset.username}/> 
  //   </React.StrictMode>
  // );
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
