'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('cnas', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      sample_id: {
        type: Sequelize.INTEGER,
        references: {
          model: 'samples',
          key: 'id'
        },
        onDelete: 'cascade'
      },
      hugo_symbol: {
        type: Sequelize.TEXT('tiny')
      },
      entrez_gene_id: {
        type: Sequelize.INTEGER
      },
      discrete: {
        type: Sequelize.INTEGER
      },
      continuous_linear: {
        type: Sequelize.FLOAT
      },
      continuous_log2: {
        type: Sequelize.FLOAT
      },
      created_at: {
        allowNull: false,
        defaultValue: new Date(),
        type: Sequelize.DATE
      },
      updated_at: {
        allowNull: false,
        defaultValue: new Date(),
        type: Sequelize.DATE
      }
    }).then(() => {
      return queryInterface.addIndex('cnas', {
        fields: ['sample_id']
      })
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('cnas');
  }
};