'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('fusions', {
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
        type: Sequelize.STRING
      },
      entrez_gene_id: {
        type: Sequelize.INTEGER
      },
      center: {
        type: Sequelize.STRING
      },
      fusion: {
        type: Sequelize.STRING
      },
      dna_support: {
        type: Sequelize.STRING
      },
      rna_support: {
        type: Sequelize.STRING
      },
      method: {
        type: Sequelize.STRING
      },
      frame: {
        type: Sequelize.STRING
      },
      comments: {
        type: Sequelize.TEXT
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
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('fusions');
  }
};