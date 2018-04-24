import React from 'react';
import Button from 'material-ui/Button';
import Dropzone from 'react-dropzone'

class SimpleMenu extends React.Component {
  onDrop = (files) => {
    this.props.callbackFromParent(files)
  }

  render() {
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
