import React from 'react'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import Upload from './upload.js'
import ClippedDrawer from './ClippedDrawer.js'
import TitlebarGridList from './TitlebarGridList.js'
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
      uploadTime: [],
      processTime: [],
      upSize: [],
      origHist: [],
      procHist: [],
      originalImages: [],
      processedImages: [],
      origTiles: [],
      procTiles: [],
      imgLoaded: false
    }
  }

  // gets processing command from drawer component
  myCallbackCommand = (cmd) => {
    this.setState({commandFromChild: cmd})
    // console.log(cmd)
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
    var object = {}

    var images = files.map(file => {
      return new Promise((resolve, reject) => {
        const reader = new window.FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
          this.setState({originalImageString: reader.result});
          resolve(reader.result); // resolve the promise
        }
      });
    });

    // Wait for the promises to resolve into the real data, THEN call the callback
    Promise.all(images).then(images_resolved => {
      object.images = images_resolved
      object.email = this.state.emailFromChild
      object.command = Number(this.state.commandFromChild)
      var date = new Date()
      var pyDate = date.toISOString()
      pyDate = pyDate.replace('T', ' ')
      pyDate = pyDate.replace('Z', '')
      object.timestamp = pyDate
      console.log(object)
      return axios.post('http://vcm-3580.vm.duke.edu:5000/process_image', object)
        .then(response => {
          console.log('response')
          console.log(response)
          this.setState({originalImages: images_resolved})
          this.setState({uploadTime: pyDate})
          this.setState({processTime: response.data.proc_times})
          this.setState({upSize: response.data.image_dims})
          this.setState({origHist: response.data.orig_hist})
          this.setState({procHist: response.data.proc_hist})
          this.setState({processedImages: response.data.proc_images})
          // creates Tiles
          const origTileData = []
          for (var i = 0; i < this.state.originalImages.length; i++) {
            // generates histogram data
            const preOData = this.state.origHist[i]
            var oData = []
            for (var m in preOData) {
              oData.push({'R': preOData[m]})
            }
            origTileData.push({img: this.state.originalImages[i],
            uptime: this.state.uploadTime, upsize: this.state.upSize[i], oHist: oData})
          }
          //console.log(origTileData)

          const procTileData = []
          for (var j = 0; j < this.state.processedImages.length; j++) {
            // cleans up response image string
            var cleanedImg = ''
            cleanedImg = this.state.processedImages[j][0]
            // removes b' from beginning and ' from end
            cleanedImg = cleanedImg.slice(2, -1)
            cleanedImg = 'data:image/jpg;base64,' + cleanedImg
            // generates histogram data
            const prePData = this.state.procHist[j]
            var pData = []
            for (var n in prePData) {
              pData.push({'R': prePData[n]})
            }
            procTileData.push({img: cleanedImg,
            proctime: this.state.processTime[j], upsize: this.state.upSize[j], pHist: pData})
          }
          //console.log(procTileData)
          this.setState({origTiles: origTileData})
          this.setState({procTiles: procTileData})
          this.setState({imgLoaded: true})
          //var cleanedImg = ''
          //cleanedImg = response.data.proc_images[0][0]
          // removes b' from beginning and ' from end
          //cleanedImg = cleanedImg.slice(2, -1)
          //cleanedImg = response.data.headers[0] + cleanedImg
          //this.setState({processedImageString: cleanedImg})
        })
        .catch(error => {
          console.log('there was error')
          console.log(error.response)
        })
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
            <Upload callbackFromUpload={this.myCallbackUpload} />
          </Toolbar>
        </AppBar>
        <ClippedDrawer callbackFromCommand={this.myCallbackCommand} callbackFromEmail={this.myCallbackEmail} />
        <TitlebarGridList oTile={this.state.origTiles} pTile={this.state.procTiles}/>
      </div>
    )
  }
}

export default App
