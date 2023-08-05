'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('svs', {
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
      annotation: {
        type: Sequelize.TEXT
      },
      breakpoint_type: {
        type: Sequelize.STRING
      },
      comments: {
        type: Sequelize.TEXT
      },
      confidence_class: {
        type: Sequelize.STRING
      },
      conn_type: {
        type: Sequelize.STRING
      },
      connection_type: {
        type: Sequelize.STRING
      },
      event_info: {
        type: Sequelize.STRING
      },
      mapq: {
        type: Sequelize.STRING
      },
      normal_read_count: {
        type: Sequelize.INTEGER
      },
      normal_variant_count: {
        type: Sequelize.INTEGER
      },
      paired_end_read_support: {
        type: Sequelize.INTEGER
      },
      site1_chrom: {
        type: Sequelize.STRING
      },
      site1_desc: {
        type: Sequelize.STRING
      },
      site1_gene: {
        type: Sequelize.STRING
      },
      site1_pos: {
        type: Sequelize.INTEGER
      },
      site2_chrom: {
        type: Sequelize.STRING
      },
      site2_desc: {
        type: Sequelize.STRING
      },
      site2_gene: {
        type: Sequelize.STRING
      },
      site2_pos: {
        type: Sequelize.INTEGER
      },
      split_read_support: {
        type: Sequelize.INTEGER
      },
      sv_class_name: {
        type: Sequelize.STRING
      },
      sv_desc: {
        type: Sequelize.STRING
      },
      sv_length: {
        type: Sequelize.INTEGER
      },
      sv_variantid: {
        type: Sequelize.INTEGER
      },
      tumor_read_count: {
        type: Sequelize.INTEGER
      },
      tumor_variant_count: {
        type: Sequelize.INTEGER
      },
      tunor_variant_count: {
        type: Sequelize.INTEGER
      },
      variant_status_name: {
        type: Sequelize.STRING
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
    return queryInterface.dropTable('svs');
  }
};