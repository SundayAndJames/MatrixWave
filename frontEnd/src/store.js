import { writable } from 'svelte/store';

//show-path模式
export let showPath = writable(false); //定义是否进入选择并显示路径的模式
export let selectedRectNumber = writable(0); //被选中的矩形节点个数
export let selectedStep = writable(0); //选择进行到的步骤序号
export let selectedNodeIds = writable([]); //保存所有被选中的节点id
export let ifSelected = writable([]); //保存节点是否被选中的状态
export let currentSelectedNodeIds = writable([]); //保存当前step选中的节点id
export let websiteArray = writable([]); //保存网站名称
export let opacityIds = writable([]); //保存被虚化的元素id
export let clickFlow1 = writable([]); //点击流数据集1
export let clickFlow2 = writable([]); //点击流数据集2
export let filterFlow1 = writable([]); //筛选得到的点击流1
export let filterFlow2 = writable([]); //筛选得到的点击流2
export let websiteIndexArray = writable([]); //网站在每一步的索引值
export let maxLinkVolumn = writable(0); //最大node流量
export let pathPositionOfNode = writable({}); //画路径时需要的Node坐标
export let pathPositionOfLink = writable({}); //画路径时需要的Link坐标