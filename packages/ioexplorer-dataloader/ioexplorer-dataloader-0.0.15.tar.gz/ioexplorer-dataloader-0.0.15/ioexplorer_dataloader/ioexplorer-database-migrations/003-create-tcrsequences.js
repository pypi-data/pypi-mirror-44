'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('tcrsequences', {
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
      sequence: {
        type: Sequelize.STRING(1024)
      },
      sequence_type: {
          type: Sequelize.ENUM('aaCDR3', 'totCDR3', 'ntCDR3', 'VJ')
      },
      reads: {
        type: Sequelize.INTEGER
      },
      freq: {
        type: Sequelize.DOUBLE
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
      return queryInterface.addIndex('tcrsequences', {
        fields: ['sample_id', 'sequence_type']
      });
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('tcrsequences');
  }
};