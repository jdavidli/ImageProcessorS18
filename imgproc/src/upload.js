import React from 'react';
import Button from 'material-ui/Button';
import Menu, { MenuItem } from 'material-ui/Menu';
import axios from 'axios';
import { UploadField } from '@navjobs/upload';

class SimpleMenu extends React.Component {
  state = {
    anchorEl: null,
    "data": [],
    "serverResponse": "",
    currentImageString: '',
  };

  handleClick = event => {
    this.setState({ anchorEl: event.currentTarget });
  };

  handleClose = () => {
    this.setState({ anchorEl: null });
    axios.get("http://vcm-3476.vm.duke.edu:5000/api/heart_rate/").then( (response) => {
    console.log(response);
    this.setState({"data": response.data});
    })
  };

  onUpload = (files) => {
    const reader = new FileReader()
    const file = files[0]
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      console.log(reader.result);
      this.setState({currentImageString: reader.result});
    }
  }

  render() {
    const { anchorEl } = this.state;

    return (
      <div>
        <Button variant='raised' Button color='inherit'
          aria-owns={anchorEl ? 'simple-menu' : null}
          aria-haspopup="true"
          onClick={this.handleClick}
        >
          Upload
        </Button>
        <Menu
          id="simple-menu"
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={this.handleClose}
        >
          <UploadField onFiles={this.onUpload}><MenuItem onClick={this.handleClose}>Image</MenuItem></UploadField>
          <img src={this.state.currentImageString} />
          <MenuItem onClick={this.handleClose}>Image List</MenuItem>
          <MenuItem onClick={this.handleClose}>ZIP Archive</MenuItem>
        </Menu>
      </div>
    );
  }
}

export default SimpleMenu;
