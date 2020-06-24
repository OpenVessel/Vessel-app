const path = require('path'); // path is Node.js utility module // require Node.js alows extract contents from modules.export object
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');

const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
  .BundleAnalyzerPlugin;
const { CleanWebpackPlugin } = require('clean-webpack-plugin');


const resolve = require('path').resolve;
const vtkRules = require('vtk.js/Utilities/config/dependency.js').webpack.core.rules;

//////////CONFIG 
const config = { // dirname is global variable containing the name of dir that script resides in
    devtool: 'eval-source-map',
    entry: __dirname + '/js/index.jsx', // for VTK entry point is ./src/index.js
 output:{ //resolve Promise request to function call back
      path: resolve('../static/js'), // goes to the public directory 
      filename: 'bundle.js', //
      publicPath: resolve('../static/js')
},
 resolve: {
  extensions: ['.js','.jsx','.css']
 },

 module: { ///////////////////////////////// MODULES
    rules: [
        {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        
        loader: "babel-loader",
      
        query:{ 
            presets:[ "@babel/preset-react", '@babel/preset-env']
        }
    }].concat(vtkRules),
   }
};
module.exports = config;



/*
const config = {
    entry:  __dirname + '/js/dicom_viewer.jsx',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: [".js", ".jsx", ".css"]
    },
    module: {
        rules: [
            {
                test: /\.jsx?/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: 'css-loader',
                })
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: 'file-loader'
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin('styles.css'),
    ]
};

module.exports = config;*/