import React from 'react';
import Button from 'material-ui/Button';
import Menu, { MenuItem } from 'material-ui/Menu';
import axios from 'axios';
import Dropzone from 'react-dropzone'

class SimpleMenu extends React.Component {
  state = {
    "data": [],
    "serverResponse": "",
    currentImageString: '',
    files: []
  };

  onDrop = (files) => {
    this.setState({
      files
    });

    files.forEach(file => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
            console.log(reader.result)
            // do whatever you want with the file content
        };
        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');
    });
    console.log(files)
    console.log('files')
  }


  render() {
    const { anchorEl } = this.state;
    const dropzoneStyle = {
    width  : "100%",
    height : "100%",
    border : "0px solid black"
};

    return (
      <div>
        <Dropzone onDrop={this.onDrop} style={dropzoneStyle}>
          <Button variant='raised' Button color='inherit'>
            Upload
          </Button>
        </Dropzone>
      </div>
    );
  }
}

export default SimpleMenu;
