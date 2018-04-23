import React from 'react';
import Button from 'material-ui/Button';
import axios from 'axios';
import Dropzone from 'react-dropzone'

class SimpleMenu extends React.Component {
  state = {
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
            const formData = new FormData();
            formData.append("file", reader.result);
            formData.append("upload_preset", "ex6elkh6"); // Replace the preset name with your own
            formData.append("api_key", "436934996138467"); // Replace API key with your own Cloudinary key
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
    console.log(files)
    console.log('files')
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
