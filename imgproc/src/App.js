import React from 'react'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import Upload from './upload.js'
import ClippedDrawer from './ClippedDrawer.js'
import axios from 'axios';

class App extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      filesDataFromChild: []
    }
  }

  myCallback = (files) => {
    this.setState({filesDataFromChild: files});
    console.log(files)

    files.forEach(file => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
            console.log(reader.result)
            const formData = new FormData();
            formData.append("file", reader.result);
            formData.append("upload_preset", "ex6elkh6");
            formData.append("api_key", "436934996138467");
            formData.append("timestamp", (Date.now() / 1000) | 0);

            // Make an AJAX upload request using Axios (replace Cloudinary URL below with your own)
            return axios.post("https://api.cloudinary.com/v1_1/dikxvn5xi/image/upload", formData, {
              headers: { "X-Requested-With": "XMLHttpRequest" },
            }).then(response => {
              const data = response.data;
              const fileURL = data.secure_url // You should store this URL for future references in your app
              console.log(data);
            })
            // do whatever you want with the file content
        };
        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');
    });
}

  render () {
    return (
      <div>
        <AppBar position='absolute'>
          <Toolbar>
            <Typography variant='title' color='inherit' style={{flex: 1}}>
            Image Processor
            </Typography>
            <Upload callbackFromParent={this.myCallback}/>
          </Toolbar>
        </AppBar>
        <ClippedDrawer />
      </div>
    )
  }
}

export default App
