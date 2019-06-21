<template>
<div></div>
</template>

<script>
import go from "gojs";
var $ = go.GraphObject.make; // for conciseness in defining templates
export default {
    name: "diagram",
    props: ["modelData"], // accept model data as a parameter
    data: function () {
        return {
            diagram: null,
            dialogFormVisible: false
        };
    },
    mounted: function () {
        var myDiagram = $(go.Diagram, this.$el, {
            "grid.visible": true,
            "grid.gridCellSize": new go.Size(30, 30),
            initialContentAlignment: go.Spot.Center, // 居中显示Diagram内容
            "undoManager.isEnabled": true, // 打开Ctrl-Z撤销和Ctrl-Y重做功能
            isReadOnly: true,
            contentAlignment: go.Spot.Center,
            autoScale: go.Diagram.Uniform, //自适应
            "toolManager.mouseWheelBehavior": go.ToolManager.WheelNone, //鼠标滚轮事件禁止
            "draggingTool.isGridSnapEnabled": true,
            "resizingTool.isGridSnapEnabled": true,
            "rotatingTool.snapAngleMultiple": 90,
            "rotatingTool.snapAngleEpsilon": 45
        });
        // define the node template
        myDiagram.nodeTemplate = $(
            go.Node,
            "Auto",
            new go.Binding("location", "loc"), {
                locationSpot: go.Spot.Center,
                toEndSegmentLength: 30,
                fromEndSegmentLength: 30
            },
            $(go.Shape, "Rectangle", {
                name: "OBJSHAPE",
                fill: "white",
                desiredSize: new go.Size(30, 30)
            }),
            $(
                go.TextBlock, {
                    margin: 4
                },
                new go.Binding("text", "key")
            )
        );

        // define a second kind of Node:
        myDiagram.nodeTemplateMap.add(
            "Terminal",
            $(
                go.Node,
                "Spot", {
                    deletable: false
                },
                $(go.Shape, "DirectData", {
                    width: 55,
                    height: 55,
                    stroke: null
                }),
                $(
                    go.TextBlock, {
                        font: "10pt Verdana, sans-serif"
                    },
                    new go.Binding("text")
                )
            )
        );

        //流程
        myDiagram.nodeTemplateMap.add(
            "Process",
            $(
                go.Node,
                "Auto", {
                    locationSpot: new go.Spot(0.5, 0.5),
                    locationObjectName: "SHAPE",
                    resizable: true,
                    resizeObjectName: "SHAPE"
                },
                new go.Binding("location", "pos", go.Point.parse).makeTwoWay(
                    go.Point.stringify
                ),
                $(
                    go.Shape,
                    "Cylinder1", {
                        name: "SHAPE",
                        strokeWidth: 2,
                        fill: $(go.Brush, "Linear", {
                            start: go.Spot.Left,
                            end: go.Spot.Right,
                            0: "gray",
                            0.5: "white",
                            1: "gray"
                        }),
                        minSize: new go.Size(50, 50),
                        portId: ""
                        // fromSpot: go.Spot.AllSides,
                        // toSpot: go.Spot.AllSides
                    },
                    new go.Binding("desiredSize", "size", go.Size.parse).makeTwoWay(
                        go.Size.stringify
                    )
                ),
                $(
                    go.TextBlock, {
                        alignment: go.Spot.Center,
                        textAlign: "center",
                        margin: 5,
                        editable: true
                    },
                    new go.Binding("text").makeTwoWay()
                )
            )
        );
        //数据库
        myDiagram.nodeTemplateMap.add(
            "DataBase",
            $(
                go.Node,
                "Auto", {
                    locationSpot: new go.Spot(0.5, 0.5),
                    locationObjectName: "SHAPE",
                    resizable: true,
                    resizeObjectName: "SHAPE"
                },
                new go.Binding("location", "pos", go.Point.parse).makeTwoWay(
                    go.Point.stringify
                ),
                $(
                    go.Shape,
                    "DataBase", {
                        name: "SHAPE",
                        strokeWidth: 2,
                        fill: $(go.Brush, "Linear", {
                            start: go.Spot.Left,
                            end: go.Spot.Right,
                            0: "gray",
                            0.5: "white",
                            1: "gray"
                        }),
                        minSize: new go.Size(50, 50),
                        portId: ""
                        // fromSpot: go.Spot.AllSides,
                        // toSpot: go.Spot.AllSides
                    },
                    new go.Binding("desiredSize", "size", go.Size.parse).makeTwoWay(
                        go.Size.stringify
                    )
                ),
                $(
                    go.TextBlock, {
                        alignment: go.Spot.Center,
                        textAlign: "center",
                        margin: 5,
                        editable: true
                    },
                    new go.Binding("text").makeTwoWay()
                )
            )
        );
        //文件
        myDiagram.nodeTemplateMap.add(
            "File",
            $(
                go.Node,
                "Auto", {
                    locationSpot: new go.Spot(0.5, 0.5),
                    locationObjectName: "SHAPE",
                    resizable: true,
                    resizeObjectName: "SHAPE"
                },
                new go.Binding("location", "pos", go.Point.parse).makeTwoWay(
                    go.Point.stringify
                ),
                $(
                    go.Shape,
                    "BpmnEventConditional", {
                        name: "SHAPE",
                        strokeWidth: 1,
                        fill: $(go.Brush, "Linear", {
                            start: go.Spot.Left,
                            end: go.Spot.Right
                            // 0: "gray",
                            // 0.5: "white",
                            // 1: "gray"
                        }),
                        minSize: new go.Size(50, 50),
                        portId: ""
                        // fromSpot: go.Spot.AllSides,
                        // toSpot: go.Spot.AllSides
                    },
                    new go.Binding("desiredSize", "size", go.Size.parse).makeTwoWay(
                        go.Size.stringify
                    )
                ),
                $(
                    go.TextBlock, {
                        alignment: go.Spot.Center,
                        textAlign: "center",
                        margin: 5,
                        editable: true
                    },
                    new go.Binding("text").makeTwoWay()
                )
            )
        );

        /**
         * group定义
         *
         */
        myDiagram.groupTemplate = $(
            go.Group,
            "Spot", {
                // adornment when a group is selected
                selectionAdornmentTemplate: $(
                    go.Adornment,
                    "Auto",
                    $(go.Shape, "Rectangle", {
                        fill: null,
                        stroke: "dodgerblue",
                        strokeWidth: 3
                    }),
                    $(go.Placeholder)
                ),
                toSpot: go.Spot.AllSides, // links coming into groups at any side
                toEndSegmentLength: 30,
                fromEndSegmentLength: 30
            },
            $(
                go.Panel,
                "Auto",
                $(
                    go.Shape,
                    "Rectangle", {
                        name: "OBJSHAPE",
                        parameter1: 14,
                        fill: "rgba(255,0,0,0.10)"
                    },
                    new go.Binding("desiredSize", "ds")
                ),
                $(go.Placeholder, {
                    padding: 16
                })
            ),
            $(
                go.TextBlock, {
                    name: "GROUPTEXT",
                    alignment: go.Spot.TopLeft,
                    alignmentFocus: new go.Spot(0, 0, 4, 4),
                    font: "Bold 10pt Sans-Serif"
                },
                new go.Binding("text")
            )
        );
        /**
         *
         * 连线定义
         *
         */
        myDiagram.linkTemplate = $(
            go.Link, {
                routing: go.Link.Orthogonal,
                curve: go.Link.JumpGap,
                corner: 2,
                // reshapable: true,
                toShortLength: 7
            },
            new go.Binding("points").makeTwoWay(),
            // mark each Shape to get the link geometry with isPanelMain: true
            $(go.Shape, {
                isPanelMain: true,
                stroke: "black",
                strokeWidth: 5
            }),
            $(go.Shape, {
                isPanelMain: true,
                stroke: "gray",
                strokeWidth: 3
            }),
            $(go.Shape, {
                isPanelMain: true,
                stroke: "white",
                strokeWidth: 1,
                name: "PIPE",
                strokeDashArray: [10, 10]
            }),
            $(go.Shape, {
                toArrow: "Triangle",
                fill: "black",
                stroke: null
            }),
            $(
                go.Panel,
                "Auto",
                // $(go.Shape, // the label background, which becomes transparent around the edges
                //     {
                //         fill: $(go.Brush, "Radial", {
                //             0: "rgb(240, 240, 240)",
                //             0.3: "rgb(240, 240, 240)",
                //             1: "rgba(240, 240, 240, 0)"
                //         }),
                //         stroke: null
                //     }, ),
                $(
                    go.TextBlock, // the label text
                    {
                        textAlign: "center",
                        font: "9pt helvetica, arial, sans-serif",
                        margin: 4,
                        editable: true // enable in-place editing
                    },
                    // editing the text automatically updates the model data
                    new go.Binding("text").makeTwoWay()
                )
            )
        );

        /***************连线定义终止*************** */

        //添加图监听，点击跳转路由
        myDiagram.addDiagramListener("ObjectSingleClicked", e => {
            this.$router.push({
                path: "/exhibision-page/" + e.subject.part.data.key
            });
        });

        var model = $(go.GraphLinksModel);
        model.nodeDataArray = [
            // 必须有"key"和"parent"的字段名,
            // 你还可以添加任何需要的其他字段
            {
                key: "P1",
                text: "数据清洗",
                category: "Process",
                group: "G1",
                pos: "0 50"
            },
            {
                key: "D1",
                text: "存储模块HBase",
                category: "DataBase",
                group: "G1",
                pos: "150 0"
            },
            {
                key: "P2",
                text: "统计模块",
                category: "Process",
                group: "G1",
                pos: "150 100"
            },
            {
                key: "D2",
                text: "CSV数据",
                category: "File",
                pos: "300 50"
            },
            {
                key: "P3",
                text: "模型训练",
                category: "Process",
                pos: "400 50",
                group: "G2"
            },
            {
                key: "D3",
                text: "模型持久化",
                category: "DataBase",
                pos: "500 50",
                group: "G2"
            },
            {
                key: "D5",
                text: "指标数据库",
                category: "DataBase",
                pos: "50 275"
            },
            {
                key: "D4",
                text: "推荐原料库",
                category: "DataBase",
                pos: "50 350"
            },
            {
                key: "P4",
                text: "召回",
                category: "Process",
                pos: "400 300",
                group: "G3"
            },
            {
                key: "P6",
                text: "排序",
                category: "Process",
                pos: "300 300",
                group: "G3"
            },
            {
                key: "P7",
                text: "指标计算",
                category: "Process",
                pos: "200 275",
                group: "G3"
            },
            {
                key: "P8",
                text: "规则",
                category: "Process",
                pos: "200 350",
                group: "G3"
            },
            {
                key: "P9",
                text: "测试服务请求",
                category: "Process",
                pos: "-75 250",
                group: "G4"
            },
            {
                key: "P10",
                text: "特征",
                category: "Process",
                pos: "500 300",
                group: "G3"
            },
            {
                key: "G1",
                text: "数据清洗模块",
                isGroup: true
            },
            {
                key: "G2",
                text: "离线计算子模块",
                isGroup: true
            },
            {
                key: "G3",
                text: "近线计算子模块",
                isGroup: true
            },
            {
                key: "G4",
                text: "在线计算子服务",
                isGroup: true
            }
            // {
            //     key: "P5",
            //     text: "管理子服务",
            //     category: "Process",
            //     //isGroup: true,
            //     pos: "85 210",
            // },
        ];
        model.linkDataArray = [{
                from: "P1",
                to: "D1",
                key: "L1"
            },
            {
                from: "P1",
                to: "P2",
                key: "L1"
            },
            {
                from: "D1",
                to: "D2",
                text: "定期生成",
                key: "L1"
            },
            {
                from: "D1",
                to: "P2",
                key: "L1"
            },
            {
                from: "D2",
                to: "P3",
                key: "L1"
            },
            {
                from: "P3",
                to: "D3",
                key: "L1"
            },
            {
                from: "D2",
                to: "P10",
                text: "数据",
                key: "L1"
            },
            {
                from: "D3",
                to: "P10",
                text: "模型",
                key: "L1"
            },
            {
                from: "G1",
                to: "P5",
                text: "统计信息",
                key: "L1"
            },
            {
                from: "P4",
                to: "P6",
                key: "L1"
            },
            {
                from: "P6",
                to: "P8",
                key: "L1"
            },
            {
                from: "P8",
                to: "D4",
                key: "L1"
            },
            {
                from: "P7",
                to: "D5",
                key: "L1"
            },
            {
                from: "D4",
                to: "G4",
                key: "L1"
            },
            {
                from: "P10",
                to: "P4",
                key: "L1"
            }
        ];
        myDiagram.model = model;
        var diagram = myDiagram;
        //循环播放
        setInterval(function () {
            var oldskips = diagram.skipsUndoManager;
            diagram.skipsUndoManager = true;
            diagram.links.each(function (link) {
                var shape = link.findObject("PIPE");
                var off = shape.strokeDashOffset - 2;
                shape.strokeDashOffset = off <= 0 ? 20 : off;
            });
            diagram.skipsUndoManager = oldskips;
        }, 100);
    }
};
</script>
