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

  myCallbackCommand = (cmd) => {
    console.log(cmd)
  }

  myCallbackUpload = (files) => {
    this.setState({filesDataFromChild: files});
    var object = {};
    files.forEach(file => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
          object.images = "["+ reader.result +"]";
          object.email = "jdl@duke.edu";
          object.command = 1;
          var date = new Date();
          var pyDate = date.toISOString();
          pyDate = pyDate.replace('T',' ');
          pyDate = pyDate.replace('Z','');
          object.timestamp = pyDate;
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
        <AppBar position='fixed'>
          <Toolbar>
            <Typography variant='title' color='inherit' style={{flex: 1}}>
            Image Processor
            </Typography>
            <Upload callbackFromUpload={this.myCallbackUpload}/>
          </Toolbar>
          <ClippedDrawer callbackFromCommand={this.myCallbackCommand}/>
        </AppBar>
      </div>
    )
  }
}

export default App
