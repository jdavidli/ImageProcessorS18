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
      filesDataFromChild: [],
      commandFromChild: ''
    }
  }

  getCommand = (command) => {
    console.log(command)
  }

  myCallback = (files) => {
    this.setState({filesDataFromChild: files});
    console.log(files)

    files.forEach(file => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
          var object = {};
          object.images = reader.result;
          object.email = "jdl@duke.edu";
          object.command = 1;
          object.timestamp = Date.now();
            console.log(object)
            return axios.post("http://vcm-3580.vm.duke.edu:5000/process_image", object)
            .then(response => {
              console.log(response);
            })
            .catch(error => {
              console.log(error.response)
            })
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
