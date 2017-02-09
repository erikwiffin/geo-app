/* global __dirname */
var webpack = require('webpack');
var CompressionPlugin = require("compression-webpack-plugin");
var path = require('path');

var buildPath = path.resolve(__dirname, 'geo_app', 'static', 'build');
var assetsPath = path.resolve(__dirname, 'assets');
var nodePath = path.resolve(__dirname, 'node_modules');

module.exports = {
    devtool: 'inline-source-map',

    entry: {
        app: [path.resolve(assetsPath, 'scripts', 'main.js')],
        styles: [
            path.resolve(assetsPath, 'styles', 'main.less'),
        ],
        vendor: [
            'jquery',
            'moment',
            'underscore',
        ],
    },
    output: {
        path: buildPath,
        filename: '[name].bundle.js',
        publicPath: '/static/build/',
    },
    module: {
        rules: [
            {
                test: /\.less$/,
                use: ['style-loader', 'css-loader', 'less-loader'],
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
            // the url-loader uses DataUrls.
            // the file-loader emits files.
            {
                test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
                use: 'url-loader?limit=10000&mimetype=application/font-woff',
            },
            {
                test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
                use: 'url-loader?limit=10000&mimetype=application/octet-stream',
            },
            {
                test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
                use: 'file-loader',
            },
            {
                test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
                use: 'url-loader?limit=10000&mimetype=image/svg+xml',
            },
        ],
    },
    plugins: [
        new webpack.optimize.CommonsChunkPlugin({
            name: 'vendor',
            filename: 'vendor.bundle.js',
            minChunks: Infinity,
            chunks: ['app', 'vendor'],
        }),
        new CompressionPlugin(),
    ],
    node: {
        fs: 'empty', // avoids error messages
    },
};
