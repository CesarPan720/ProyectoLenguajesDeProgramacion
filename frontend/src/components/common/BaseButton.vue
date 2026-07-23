<script setup>
defineProps({
  type: { type: String, default: 'button' },
  variant: { type: String, default: 'primary' }
})

const variantes = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800'
}
</script>

<template>
  <button
    :type="type"
    class="px-4 py-2 rounded-md font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
    :class="variantes[variant]"
  >
    <slot />
  </button>
</template>
