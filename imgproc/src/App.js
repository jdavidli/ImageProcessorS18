import React from 'react'
import AppBar from 'material-ui/AppBar'
import Toolbar from 'material-ui/Toolbar'
import Typography from 'material-ui/Typography'
import Upload from './upload.js'
import ClippedDrawer from './ClippedDrawer.js'
import TitlebarGridList from './TitlebarGridList.js'
import axios from 'axios'
import Button from 'material-ui/Button'

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
        const reader = new window.FileReader()
        reader.readAsDataURL(file)
        reader.onloadend = () => {
          this.setState({originalImageString: reader.result})
          resolve(reader.result) // resolve the promise
        }
      })
    })

    // Wait for the promises to resolve into the real data, THEN call the callback
    Promise.all(images).then(imagesResolved => {
      object.images = imagesResolved
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
          this.setState({originalImages: response.data.orig_images})
          this.setState({uploadTime: pyDate})
          this.setState({processTime: response.data.proc_times})
          this.setState({upSize: response.data.image_dims})
          this.setState({origHist: response.data.orig_hist})
          this.setState({procHist: response.data.proc_hist})
          this.setState({processedImages: response.data.proc_images})
          // creates Tiles
          const origTileData = []
          for (var i = 0; i < this.state.originalImages.length; i++) {
            // cleans up response image string
            var cleanedOImg = ''
            cleanedOImg = this.state.originalImages[i]
            // removes b' from beginning and ' from end
            cleanedOImg = cleanedOImg.slice(2, -1)
            cleanedOImg = 'data:image/jpg;base64,' + cleanedOImg
            // generates histogram data
            const preOData = this.state.origHist[i]
            var oData = []
            for (var m in preOData) {
              oData.push({'R': preOData[m]})
            }
            origTileData.push({img: cleanedOImg,
              uptime: this.state.uploadTime,
              upsize: this.state.upSize[i][1] + ' x ' + this.state.upSize[i][0],
              oHist: oData})
          }
          // console.log(origTileData)

          const procTileData = []
          for (var j = 0; j < this.state.processedImages.length; j++) {
            // cleans up response image string
            var cleanedPImg = ''
            cleanedPImg = this.state.processedImages[j][0]
            // removes b' from beginning and ' from end
            cleanedPImg = cleanedPImg.slice(2, -1)
            cleanedPImg = 'data:image/jpg;base64,' + cleanedPImg
            // generates histogram data
            const prePData = this.state.procHist[j]
            var pData = []
            for (var n in prePData) {
              pData.push({'R': prePData[n]})
            }
            procTileData.push({img: cleanedPImg,
              proctime: this.state.processTime[j],
              upsize: this.state.upSize[j][1] + ' x ' + this.state.upSize[j][0],
              pHist: pData})
          }
          // console.log(procTileData)
          this.setState({origTiles: origTileData})
          this.setState({procTiles: procTileData})
        })
        .catch(error => {
          console.log('There was an error')
          console.log(error.response.data.message)
        })
    })
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
        <TitlebarGridList oTile={this.state.origTiles} pTile={this.state.procTiles} />
      </div>
    )
  }
}

export default App
