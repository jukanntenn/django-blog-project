module.exports = {
    presets: [
        [
            '@vue/cli-plugin-babel/preset',
            {
                // false:不在代码中使用polyfills，表现形式和@babel/preset-latest一样，当使用ES6+语法及API时，在不支持的环境下会报错。
                // 'usage':在文件需要的位置单独按需引入，可以保证在每个bundler中只引入一份
                // 'entry': 在入口处引入，一般 entry 打包后体积会比 usage 大
                useBuiltIns: false,
            },
        ],
    ],
};
