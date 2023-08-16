<script>
  export let stepNumber = 1;
  export let radius = 7.5;
  export let websiteName = [
    "myweb.com",
    "youtube.com",
    "hunan.com",
    "zhejiang.com",
    "jiangxi.com",
  ];
  export let positionX = 200;
  export let positionY = 50;
  let colors = [
    "rgb(173, 220, 230)", // 淡蓝色
    "rgb(112, 128, 144)", // 石板灰
    "rgb(165, 42, 42)", // 棕色
    "rgb(205, 92, 92)", // 印度红
    "rgb(128, 128, 0)", // 橄榄色
    "rgb(173, 255, 47)", // 黄绿色
    "rgb(60, 179, 113)", // 军绿色
    "rgb(238, 130, 238)", // 紫罗兰色
    "rgb(255, 182, 193)", // 浅粉红
    "rgb(0, 128, 192)", // 坦帕湾蓝
  ];
</script>

{#if stepNumber % 2 == 0}
  {#each websiteName as item, i}
    <circle
      cx={positionX + radius}
      cy={positionY + 2 * i * radius + radius}
      r={radius}
      fill={colors[i % 5]}
    />
    <text
      class={websiteName[i]}
      id="text{stepNumber}{i}"
      x={positionX + 2 * radius}
      y={positionY + 2 * i * radius + 1.5 * radius}
      fill="black">{item}</text
    >
  {/each}
{:else}
  {#each websiteName as item, i}
    <circle
      cx={positionX + 2 * i * radius + radius}
      cy={positionY + radius}
      r={radius}
      fill={colors[i % 5]}
    />
    <text
      class={websiteName[i]}
      id="text{stepNumber}{i}"
      x={positionX + 2 * i * radius + 0.5 * radius}
      y={positionY + 2 * radius}
      transform="rotate(90 {positionX +
        2 * i * radius +
        0.5 * radius},{positionY + 2 * radius})"
      fill="black">{item}</text
    >
  {/each}
{/if}

<style>
  text {
    font-family: Arial, sans-serif;
    font-size: 14px;
    fill: #333;
  }
</style>
