import React from 'react'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import Upload from './upload.js'
import ClippedDrawer from './ClippedDrawer.js'
import axios from 'axios'

class App extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      filesDataFromChild: [],
      commandFromChild: '1',
      emailFromChild: '',
      processedResponse: null,
      originalImageString: '',
      processedImageString: '',
      uploadTime: '',
      processTime: '',
      upSize: '',
      origHist: []
    }
  }

  // gets processing command from drawer component
  myCallbackCommand = (cmd) => {
    this.setState({commandFromChild: cmd})
    console.log(cmd)
  }

  // get the value from email textfield onChange event
  myCallbackEmail = (e) => {
    this.setState({
      emailFromChild: e.target.value
    })
    // console.log(e.target.value)
  }

  upSizeCallback = (width, height) => {
    console.log(width)
    console.log(height)
  }

  // gets uploaded file information from upload button
  myCallbackUpload = (files) => {
    this.setState({filesDataFromChild: files})
    const file = files.find(f => f)
    const i = new Image()
    var object = {}
    var images = []
    i.onload = () => {
      const reader = new window.FileReader()
      reader.readAsDataURL(file)
      reader.onloadend = () => {
        this.setState({originalImageString: reader.result})
        // gets image size
        this.setState({upSize: i.width + ' x ' + i.height})
        console.log(i.width, i.height);
        console.log(this.state.upSize)

        // pushes image string into array
        images.push(reader.result)
        object.images = images
        object.email = this.state.emailFromChild
        object.command = Number(this.state.commandFromChild)
        var date = new Date()
        var pyDate = date.toISOString()
        pyDate = pyDate.replace('T', ' ')
        pyDate = pyDate.replace('Z', '')
        object.timestamp = pyDate
        this.setState({uploadTime: pyDate})
        console.log(object)
        return axios.post('http://vcm-3580.vm.duke.edu:5000/process_image', object)
          .then(response => {
            console.log(response)
            this.setState({processTime: response.data.proc_times})
            var cleanedImg = ''
            cleanedImg = response.data.proc_images[0][0]
            // removes b' from beginning and ' from end
            cleanedImg = cleanedImg.slice(2, -1)
            cleanedImg = response.data.headers[0] + cleanedImg
            this.setState({processedImageString: cleanedImg})
            this.setState({origHist: response.data.orig_hist})
          })
          .catch(error => {
            console.log(error.response)
          })
      }
      reader.onabort = () => console.log('file reading was aborted')
      reader.onerror = () => console.log('file reading has failed')
    }
    i.src = file.preview


  }

  render () {
    return (
      <div>
        <AppBar position='fixed'>
          <Toolbar>
            <Typography variant='title' color='inherit' style={{flex: 1}}>
            Image Processor
            </Typography>
            <Upload callbackFromUpload={this.myCallbackUpload} />
          </Toolbar>
        </AppBar>
        <ClippedDrawer callbackFromCommand={this.myCallbackCommand} callbackFromEmail={this.myCallbackEmail}
          oImgParent={this.state.originalImageString} pImgParent={this.state.processedImageString}
          uTime={this.state.uploadTime} pTime={this.state.processTime} uSize={this.state.upSize}
          oHist={this.state.origHist}/>
      </div>
    )
  }
}

export default App
