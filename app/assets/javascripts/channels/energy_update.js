App.energy_update = App.cable.subscriptions.create("EnergyUpdateChannel", {
  connected: function() {
    console.log('connected');
  },
  disconnected: function() {},
  received: function(data) {
    console.log(data);
    consumeChart.data.datasets[0].data.push(data.message.consumption);
    consumeChart.data.labels.push(data.message.time);
    consumeChart.update()
  },
  test: function(){
    this.perform('test')
  }
});
