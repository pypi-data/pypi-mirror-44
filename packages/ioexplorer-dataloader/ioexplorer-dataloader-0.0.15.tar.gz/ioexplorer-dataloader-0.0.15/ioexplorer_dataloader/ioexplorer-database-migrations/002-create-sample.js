'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('samples', {
      id: {
        primaryKey: true,
        autoIncrement: true,
        type: Sequelize.INTEGER,
        allowNull: false
      },
      subject_id: {
        type: Sequelize.INTEGER,
        references: {
          model: 'subjects',
          key: 'id'
        },
        onDelete: 'cascade'
      },
      sample_label: {
        type: Sequelize.STRING,
      },
      cancer_type: {
        type: Sequelize.STRING
      },
      cancer_type_detailed: {
        type: Sequelize.STRING
      },
      sample_type: {
        type: Sequelize.STRING
      },
      sample_class: {
        type: Sequelize.STRING
      },
      gene_panel: {
        type: Sequelize.STRING
      },
      sample_cover: {
        type: Sequelize.INTEGER
      },
      tumor_purity: {
        type: Sequelize.FLOAT
      },
      oncotree_code: {
        type: Sequelize.STRING
      },
      msi_score: {
        type: Sequelize.FLOAT
      },
      msi_type: {
        type: Sequelize.STRING
      },
      institute: {
        type: Sequelize.STRING
      },
      somatic_status: {
        type: Sequelize.STRING
      },
      // Exome Variables
      mutation_count: {
        type: Sequelize.INTEGER,
      },
      mutation_count_synon_incl: {
        type: Sequelize.INTEGER,
      },
      indel_count: {
        type: Sequelize.INTEGER,
      },
      log10_mutation_count: {
        type: Sequelize.FLOAT,
      },
      tmb: {
        type: Sequelize.FLOAT,
      },
      tmb_syn: {
        type: Sequelize.FLOAT,
      },
      tmb_indel: {
        type: Sequelize.FLOAT,
      },
      log_tmb: {
        type: Sequelize.FLOAT,
      },
      log_tmb_syn: {
        type: Sequelize.FLOAT,
      },
      log_tmb_indel: {
        type: Sequelize.FLOAT,
      },
      neoantigen_count: {
        type: Sequelize.INTEGER,
      },
      log_neoantigen_count: {
        type: Sequelize.FLOAT,
      },
      neopeptide_count: {
        type: Sequelize.INTEGER,
      },
      log_neopeptide_count: {
        type: Sequelize.FLOAT,
      },
      aging_signature: {
        type: Sequelize.FLOAT,
      },
      uv_signature: {
        type: Sequelize.FLOAT,
      },
      davoli_scna: {
        type: Sequelize.FLOAT,
      },
      fraction_genome_cna: {
        type: Sequelize.FLOAT,
      },
      fga: {
        type: Sequelize.FLOAT
      },
      // RNA stuff
      b_cells_naive: {
        type: Sequelize.FLOAT,
      },
      b_cells_memory: {
        type: Sequelize.FLOAT,
      },
      plasma: {
        type: Sequelize.FLOAT,
      },
      t_cells_cd8: {
        type: Sequelize.FLOAT,
      },
      t_cells_cd4_naive: {
        type: Sequelize.FLOAT,
      },
      t_cells_cd4_resting: {
        type: Sequelize.FLOAT,
      },
      t_cells_cd4_activated: {
        type: Sequelize.FLOAT,
      },
      t_cells_follicular_helper: {
        type: Sequelize.FLOAT,
      },
      t_cells_regulator: {
        type: Sequelize.FLOAT,
      },
      natural_killer_resting: {
        type: Sequelize.FLOAT,
      },
      natural_killer_activated: {
        type: Sequelize.FLOAT,
      },
      monocytes: {
        type: Sequelize.FLOAT,
      },
      macrophages_m0: {
        type: Sequelize.FLOAT,
      },
      macrophages_m1: {
        type: Sequelize.FLOAT,
      },
      macrophages_m2: {
        type: Sequelize.FLOAT,
      },
      macrophages_m2: {
        type: Sequelize.FLOAT,
      },
      dendritic_cells_activated: {
        type: Sequelize.FLOAT,
      },
      neutrophils_cibersort: {
        type: Sequelize.FLOAT,
      },
      apm2: {
        type: Sequelize.FLOAT,
      },
      angiogenesis: {
        type: Sequelize.FLOAT,
      },
      b_cells: {
        type: Sequelize.FLOAT,
      },
      cd8_t_cells: {
        type: Sequelize.FLOAT,
      },
      ctla4: {
        type: Sequelize.FLOAT,
      },
      cytotoxic_cells: {
        type: Sequelize.FLOAT,
      },
      dc: {
        type: Sequelize.FLOAT,
      },
      macrophages: {
        type: Sequelize.FLOAT,
      },
      nk_cd56_bright_cells: {
        type: Sequelize.FLOAT,
      },
      nk_cd56_dim_cells: {
        type: Sequelize.FLOAT,
      },
      nk_cells: {
        type: Sequelize.FLOAT,
      },
      neutrophils_ssgsea: {
        type: Sequelize.FLOAT,
      },
      pd1: {
        type: Sequelize.FLOAT,
      },
      pdl1: {
        type: Sequelize.FLOAT,
      },
      t_cells: {
        type: Sequelize.FLOAT,
      },
      t_helper_cells: {
        type: Sequelize.FLOAT,
      },
      tcm_cells: {
        type: Sequelize.FLOAT,
      },
      tem_cells: {
        type: Sequelize.FLOAT,
      },
      tfh_cells: {
        type: Sequelize.FLOAT,
      },
      tgd_cells: {
        type: Sequelize.FLOAT,
      },
      th1_cells: {
        type: Sequelize.FLOAT,
      },
      th17_cells: {
        type: Sequelize.FLOAT,
      },
      th2_cells: {
        type: Sequelize.FLOAT,
      },
      treg_cells: {
        type: Sequelize.FLOAT,
      },
      adc: {
        type: Sequelize.FLOAT,
      },
      idc: {
        type: Sequelize.FLOAT,
      },
      pdc: {
        type: Sequelize.FLOAT,
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
      return queryInterface.addIndex('samples', {
        fields: ['subject_id']
      });
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('samples');
  }
};