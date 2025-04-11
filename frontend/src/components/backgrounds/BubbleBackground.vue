<!--Background with lava lamp bubbles-->
<template>
  <div class="relative  component-container ">
    <div class="bubbles" style="filter: url('#blob'); z-index: -6;">
      <div
          v-for="i in 128"
          :key="i"
          :style="{
            '--size': `${2 + Math.random() * 6}rem`, // Bubble size
            '--distance': `${10+ Math.random() * 100}rem`, // How far the bubbles reach up
            '--position': `${-5 + Math.random() * 110}%`,  // Horizontal distribution
            '--time': `${8 + Math.random() * 5}s`, // How fast they move
                        '--delay': `${-1 * (2 + Math.random() * 15)}s`,   // Random delay so they don’t all start at once
            '--skew-x': `${-5 + Math.random() * 10}deg`,
            '--skew-y': `${-5 + Math.random() * 10}deg`,
            '--scale-x': `${0.8 + Math.random() * 1.5}`,
            '--scale-y': `${0.8 + Math.random() * 1.5}`,
            '--opacity': `${0.05 + Math.random() * 0.1}`,
            '--border-radius': `
                ${Math.floor(20 + Math.random() * 30)}%
                ${Math.floor(20 + Math.random() * 30)}%
                ${Math.floor(20 + Math.random() * 30)}%
                ${Math.floor(20 + Math.random() * 30)}%`
          }"
          class="bubble"
      ></div>
    </div>
    <svg class="fixed top-[100vh]">
      <defs>
        <filter id="blob">
          <feGaussianBlur in="SourceGraphic" result="blur" stdDeviation="4"/>
          <feColorMatrix
              in="blur"
              mode="matrix"
              result="blob"
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 15 -7"/>
        </filter>
      </defs>
    </svg>

  </div>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.component-container {
  width: 100vw;
  margin-top: 65vh;
  z-index: -10;
}

HTL Girls
.bubbles {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 10vh;
}

/* Bubbles Container */
.bubble {
  --distance: ${10+ Math.random() * 100}rem;
  --size: ${2 + Math.random() * 6}rem;
  --position: 110%;
  --time: ${8 + Math.random() * 5}s;
  --delay: ${-1 * (2 + Math.random() * 15)} s;
  --skew-x: ${-5 + Math.random() * 10} deg;
  --skew-y: ${-5 + Math.random() * 10} deg;
  --scale-x: ${0.8 + Math.random() * 1.5};
  --scale-y: ${0.8 + Math.random() * 1.5};
  --opacity: ${0.05 + Math.random() * 0.1};

  position: absolute;
  left: var(--position, 10%);
  width: var(--size, 4rem);
  height: var(--size, 4rem);
  background: theme('colors.primary');
  transform: translateX(-50%) skewX(var(--skew-x)) skewY(var(--skew-y)) scale(var(--scale-x), var(--scale-y));
  border-radius: 50%;
  animation: bubble-size var(--time, 4s) ease-in infinite var(--delay, 0s),
  bubble-move var(--time, 4s) ease-in infinite var(--delay, 0s);
}

/* Bubble Size Animation */
@keyframes bubble-size {
  0%,
  75% {
    width: var(--size, 4rem);
    height: var(--size, 4rem);
  }
  100% {
    width: 0;
    height: 0;
  }
}

/* Bubble Movement Animation */
@keyframes bubble-move {
  0% {
    bottom: 0;
  }
  100% {
    bottom: var(--distance, 5rem);
  }
}
</style>
